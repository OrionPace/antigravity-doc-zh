"""
Google Antigravity & Codex Documentation Daily Incremental Sync Engine
=====================================================================
Features:
1. Fetches official sitemap from https://antigravity.google/sitemap-0.xml
2. Downloads official raw Markdown endpoints at <url>.md
3. Two-Tier Hash Guard: Computes SHA-256 and compares with state/hash_manifest.json
   - If unchanged: 0 API calls, 0 Token consumed.
   - If changed/new: Enqueues only dirty pages for incremental translation.
4. Translates dirty pages via LLM API (Gemini / DeepSeek / OpenRouter / OpenAI)
   with strict terminology retention rules (CLI commands, flags, and skills are never mistranslated).
5. Writes updated files to docs/cli/ and updates state/hash_manifest.json.
"""

import os
import sys
import re
import json
import time
import hashlib
import argparse
import requests
from typing import Dict, List, Tuple, Optional

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(BASE_DIR, "state")
STATE_FILE = os.path.join(STATE_DIR, "hash_manifest.json")
DOCS_CLI_DIR = os.path.join(BASE_DIR, "docs", "cli")

SITEMAP_URL = "https://antigravity.google/sitemap-0.xml"

# Strict system prompt for translation
SYSTEM_PROMPT = """你是一个精通 Google Antigravity CLI 的资深技术专家与专业本地化翻译官。
你的任务是将指定的 Antigravity CLI 官方英文 Markdown 文档翻译为专业、流畅、地道的简体中文。

【最高原则：核心命令、变量与专有名词绝对保留英文】
Antigravity CLI 是一套高频翻阅的字典式工具书，读者需要根据文档在终端实际输入命令。因此：
1. 固化命令与 Slash Commands 绝对不翻译：
   agy, /agents, /codesearch, /credits, /diff, /permissions, /resume, /statusline, /title, /usage, /voice, /plan, /goal, /schedule, /browser, /teamwork-preview, /learn, /boost, /help, /exit, /quit 等。
2. CLI 命令行参数、Flags 与配置项 绝对不翻译：
   --headless, --help, --version, --workspace, --model, -y, -m, settings.json, config, .env, OBSIDIAN_VAULT_PATH, base_url, api_key 等。
3. 核心机制名称严格保留英文（或首次出现使用“英文（中文解释）”格式，正文保留英文，严禁单独纯直译）：
   - skill / skills（严禁单独写“技能”，可写 skill 或 skill（技能））
   - subagent / subagents（严禁单独写“子代理”，可写 subagent 或 subagent（子代理））
   - agent / agents（可写 agent 或 agent（智能体/代理））
   - artifact / artifacts（严禁单独写“人造物”，可写 artifact 或 artifact（工件/成果物））
   - MCP / Model Context Protocol（保持原样）
   - hook / hooks（保持 hook 或 hook（钩子））
   - plugin / plugins（保持 plugin 或 plugin（插件））
   - rule / rules（保持 rule 或 rule（规则））
   - sandbox（保持 sandbox 或 sandbox（沙箱））
   - headless mode（保持 headless mode 或 headless 模式（无头模式））
   - statusline（保持 statusline 或 statusline（状态栏/状态行））
   - TUI（Terminal User Interface，保持 TUI 或 TUI（终端界面））
   - workspace（保持 workspace 或 workspace（工作区））
   - tool call / tool calling（保持 tool call 或 tool call（工具调用））
   - prompt / prompting（保持 prompt 或 prompt（提示词/交互））
   - agent harness（保持 agent harness 或 agent harness（代理底座））
   - turn（保持 turn 或 turn（轮次））
4. 按键与快捷键 绝对不翻译：Ctrl+C, Ctrl+D, Tab, Esc, Enter, Shift+Enter 等。
5. 代码块、JSON 配置与终端命令输出 100% 保持原样，代码内英文注释可翻译为中文。
6. 中英文混排规范：中文与英文单词、行内代码、数字之间保留一个半角空格（盘古之白）。
7. 必须完整翻译整篇文档，严禁截断、摘要、或者遗漏任何段落！
只返回翻译后的 Markdown 文本，不要在外部包裹多余的提示词说明。"""

def slugify_filename(original_path: str) -> str:
    # E.g. "/docs/cli/commands/agents" -> "23-agents-command-agents.md"
    # Or derive from mapping
    clean = original_path.replace("/docs/cli/", "").strip("/")
    clean = clean.replace("/", "-")
    return clean + ".md"

def load_manifest() -> Dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_manifest(manifest: Dict):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def fetch_sitemap_urls(session: requests.Session) -> List[str]:
    resp = session.get(SITEMAP_URL, timeout=15)
    resp.raise_for_status()
    urls = re.findall(r"<loc>(https://antigravity.google/docs/cli/[^<]*)</loc>", resp.text)
    # Deduplicate and sort
    clean_urls = []
    seen = set()
    for u in urls:
        path = u.replace("https://antigravity.google", "").rstrip("/")
        if path and path not in seen:
            seen.add(path)
            clean_urls.append(path)
    return sorted(clean_urls)

def call_llm_translate(text: str, provider: str = "auto") -> Optional[str]:
    """Call LLM API with fallback chain: Gemini -> DeepSeek -> OpenRouter -> OpenAI"""
    gemini_key = os.environ.get("GEMINI_API_KEY")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    
    # 1. Try Gemini if available
    if (provider in ("auto", "gemini")) and gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\n--- 待翻译英文文档 ---\n\n{text}"}]}],
                "generationConfig": {"temperature": 0.2}
            }
            res = requests.post(url, json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  [WARN] Gemini API error: {e}")

    # 2. Try DeepSeek if available
    if (provider in ("auto", "deepseek")) and deepseek_key:
        try:
            url = "https://api.deepseek.com/chat/completions"
            headers = {"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"}
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"请翻译以下 Antigravity CLI 文档：\n\n{text}"}
                ],
                "temperature": 0.2
            }
            res = requests.post(url, headers=headers, json=payload, timeout=90)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"  [WARN] DeepSeek API error: {e}")

    # 3. Try OpenRouter / OpenAI
    api_key = openrouter_key or openai_key
    if (provider in ("auto", "openrouter", "openai")) and api_key:
        try:
            base_url = "https://openrouter.ai/api/v1" if openrouter_key else "https://api.openai.com/v1"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            model = os.environ.get("OPENROUTER_MODEL", "deepseek/deepseek-chat" if openrouter_key else "gpt-4o-mini")
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"请翻译以下 Antigravity CLI 文档：\n\n{text}"}
                ],
                "temperature": 0.2
            }
            res = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=90)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"  [WARN] OpenAI/OpenRouter API error: {e}")

    return None

def main():
    parser = argparse.ArgumentParser(description="Antigravity Docs Incremental Sync")
    parser.add_argument("--dry-run", action="store_true", help="Inspect differences without translating or writing")
    parser.add_argument("--force", action="store_true", help="Force re-translation of all documents")
    parser.add_argument("--provider", default="auto", choices=["auto", "gemini", "deepseek", "openrouter", "openai"])
    args = parser.parse_args()

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    print("=== Antigravity CLI Docs Incremental Sync Engine ===")
    print(f"Mode: {'DRY RUN' if args.dry_run else ('FORCE FULL' if args.force else 'INCREMENTAL')}")
    
    # 1. Fetch sitemap
    print("1. Fetching upstream sitemap...")
    try:
        upstream_paths = fetch_sitemap_urls(session)
        print(f"   Found {len(upstream_paths)} CLI docs in sitemap.")
    except Exception as e:
        print(f"   Error fetching sitemap: {e}")
        sys.exit(1)

    # 2. Check hash manifest
    manifest = load_manifest()
    dirty_pages: List[Tuple[str, str, str, str]] = [] # (path, md_url, raw_text, new_sha)

    print("2. Comparing upstream SHA-256 fingerprints with state/hash_manifest.json...")
    for path in upstream_paths:
        md_url = f"https://antigravity.google{path}.md"
        try:
            r = session.get(md_url, timeout=15)
            if r.status_code != 200:
                continue
            raw_text = r.text
            new_sha = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
            old_record = manifest.get(path, {})
            old_sha = old_record.get("sha256")
            dest_file = old_record.get("dest_file")

            if args.force or (new_sha != old_sha) or (not dest_file) or (not os.path.exists(os.path.join(BASE_DIR, dest_file))):
                dirty_pages.append((path, md_url, raw_text, new_sha))
                print(f"   [DIRTY] {path:40} (SHA: {old_sha[:8] if old_sha else 'None'} -> {new_sha[:8]})")
            else:
                pass # Unchanged!
        except Exception as e:
            print(f"   [SKIP] {path}: {e}")

    # 3. Handle dirty pages
    if not dirty_pages:
        print()
        print(">>> 0 DIRTY PAGES DETECTED! <<<")
        print("All documents are 100% up-to-date with upstream. Consumed 0 Tokens.")
        print("Exiting cleanly with code 0.")
        sys.exit(0)

    print()
    print(f"Found {len(dirty_pages)} pages requiring translation.")
    if args.dry_run:
        print("[DRY RUN] Will not call API or modify files. Exiting.")
        sys.exit(0)

    # 4. Perform translation for dirty pages
    success_count = 0
    for path, md_url, raw_text, new_sha in dirty_pages:
        print(f"Translating: {path} ({len(raw_text)} chars)...")
        translated = call_llm_translate(raw_text, provider=args.provider)
        if not translated:
            print(f"  [FAILED] No API response or keys missing for {path}. Skipping.")
            continue

        # Determine target file
        old_record = manifest.get(path, {})
        dest_rel = old_record.get("dest_file")
        if not dest_rel:
            dest_rel = f"docs/cli/{slugify_filename(path)}"
        
        target_path = os.path.join(BASE_DIR, dest_rel)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(translated)

        # Update manifest
        manifest[path] = {
            "sha256": new_sha,
            "url": md_url,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "dest_file": dest_rel
        }
        success_count += 1
        print(f"  [SAVED] -> {dest_rel}")
        time.sleep(1) # Polite rate limit

    save_manifest(manifest)
    print()
    print(f"Sync complete! Successfully updated {success_count}/{len(dirty_pages)} pages.")

if __name__ == "__main__":
    main()
