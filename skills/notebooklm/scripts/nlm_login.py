# NotebookLM(notebooklm CLI)のログインをやり直す。初回と期限切れの時だけ使う。
#
# 実行(背後実行にする。窓が開いて、保存の合図を待ち続ける):
#   Windows: & $env:USERPROFILE\.notebooklm-venv\Scripts\python.exe nlm_login.py
#   Mac:     ~/.notebooklm-venv/bin/python nlm_login.py
# 開いた Chrome の窓でログイン → ノートブック一覧が出たら、このファイルと同じフォルダに
# nlm_save_signal という空ファイルを作る → ログイン情報を保存して窓が閉じる。
# 確かめ方: notebooklm list が一覧を返すこと(auth check は当てにならない)。
#
# channel="chrome" でパソコンに入っている Chrome を使う
# (Playwright 専用の Chromium が未ダウンロードでも動くように)。
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

STORAGE_PATH = Path.home() / ".notebooklm" / "storage_state.json"
PROFILE_PATH = Path.home() / ".notebooklm" / "browser_profile"
SIGNAL_FILE = Path(__file__).with_name("nlm_save_signal")

SIGNAL_FILE.unlink(missing_ok=True)
STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_PATH), headless=False, channel="chrome",
        args=["--disable-blink-features=AutomationControlled"],
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://notebooklm.google.com/")
    while not SIGNAL_FILE.exists():
        time.sleep(1)
    STORAGE_PATH.write_text(json.dumps(browser.storage_state()), encoding="utf-8")
    browser.close()

SIGNAL_FILE.unlink(missing_ok=True)
print("saved", STORAGE_PATH)
