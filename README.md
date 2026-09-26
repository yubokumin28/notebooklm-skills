# NotebookLM Skills for Claude Code

Claude Code から Google NotebookLM(Gemini Notebook)を操作するためのスキル集です。
チャットで「NotebookLM にこの資料を入れて」「スライドを作って」と頼むだけで動きます。

| スキル | できること |
|---|---|
| `notebooklm` | ノートブックの作成・一覧、資料(ソース)の追加・削除・名前変更、質問、音声/動画/スライド/レポート等の生成とダウンロード |
| `notebooklm-slides` | 原稿ファイルからスライドを生成し、PDF と 1枚ずつの PNG に書き出すまでを1コマンドで実行 |
| `notebooklm-organize` | 全ノートブックの名前を「絵文字【カテゴリ】タイトル」形式に一括で整える |

内部では非公式ライブラリ [notebooklm-py](https://pypi.org/project/notebooklm-py/) の CLI を使います。
Google の仕様変更で突然動かなくなることがあります(下の「既知の制限」参照)。

---

## 1. 必要なもの

- Claude Code(デスクトップアプリ または CLI)
- Python 3.10 以上
- Google Chrome(ログイン用)
- NotebookLM を使える Google アカウント

## 2. インストール

### 2-1. notebooklm CLI を入れる

**Windows(PowerShell)**

```powershell
python -m venv $env:USERPROFILE\.notebooklm-venv
& $env:USERPROFILE\.notebooklm-venv\Scripts\pip.exe install "notebooklm-py[browser]" pymupdf pillow
```

**Mac / Linux**

```bash
python3 -m venv ~/.notebooklm-venv
~/.notebooklm-venv/bin/pip install "notebooklm-py[browser]" pymupdf pillow
```

### 2-2. スキルを Claude Code に置く

このリポジトリの `skills` フォルダの中身(3つのフォルダ)を、次の場所へコピーします。

- Windows: `C:\Users\<あなたのユーザー名>\.claude\skills\`
- Mac / Linux: `~/.claude/skills/`

Claude Code を開き直すとスキルが読み込まれます。

### 2-3. Google にログインする(初回と、期限切れの時だけ)

Claude Code に「NotebookLM にログインして」と頼むと、スキル内の `nlm_login.py` が Chrome の窓を開きます。
その窓で Google にログインし、ノートブック一覧が見えたら Claude に「ログインできた」と伝えてください。

ログイン情報は自分のパソコンの `~/.notebooklm/storage_state.json` にだけ保存されます。
**このファイルは絶対に他人に渡したり GitHub に上げたりしないでください**(Google アカウントに入れてしまいます)。

## 3. 使い方の例

チャットにそのまま書けば動きます。

```
NotebookLM に「営業資料」というノートブックを作って、このPDFを資料として追加して
```

```
このノートブックの資料一覧を出して、エラーになっている資料を消して
```

```
原稿.md からスライドを日本語で作って PNG に書き出して
```

```
NotebookLM のノートブック名を整理して
```

削除・生成・ダウンロードの前には、Claude が必ず確認を取ります。

## 4. 既知の制限(2026-09 時点)

| 症状 | 原因 | 対処 |
|---|---|---|
| `Authentication expired` と出る | Google のログインが期限切れ(約2週間) | もう一度ログインする |
| `auth check` は valid なのに動かない | auth check は Cookie の形しか見ていない | 動作確認は必ず `notebooklm list` で行う |
| ノートブックの `rename` が成功と出るのに名前が変わらない | 2026-07 の Gemini Notebook 刷新後の不具合(notebooklm-py 0.7.3 で確認) | `notebooklm-organize` スキルのブラウザ経由の手順を使う |
| 他人から共有されたノートブックの名前が変わらない | 権限の制約 | 対象から外す |
| 生成が失敗する | Google 側のレート制限 | 5〜10分空けて再実行 |

## 5. 安全について

- このリポジトリには API キー・Cookie・個人のファイルパスは含まれていません
- ログイン情報(`storage_state.json` と `browser_profile` フォルダ)は `.gitignore` で除外しています
- 非公式 API を使うため、Google の利用規約の範囲内で自己責任でお使いください

## ライセンス

MIT License
