---
name: notebooklm
description: Google NotebookLM(Gemini Notebook)を notebooklm CLI で操作するスキル。ノートブックの作成・一覧、資料(ソース)の追加・削除・名前変更、質問、音声/動画/スライド/レポート/クイズ等の生成とダウンロードを行う。発火トリガー: 「/notebooklm」「NotebookLMに追加して」「NotebookLMで〜を作って」「ポッドキャストを作って」「資料を消して」「ソースを追加して」「ノートブックを作って」。
---

# NotebookLM 操作

目的: NotebookLM の操作を CLI で完結させる。
成果物: 頼まれた操作(作成・追加・削除・生成・ダウンロード)が実行され、結果を読み取りコマンドで確かめた状態。

## 実行ファイルの場所

| OS | CLI | Python |
|---|---|---|
| Windows | `$env:USERPROFILE\.notebooklm-venv\Scripts\notebooklm.exe` | `$env:USERPROFILE\.notebooklm-venv\Scripts\python.exe` |
| Mac / Linux | `~/.notebooklm-venv/bin/notebooklm` | `~/.notebooklm-venv/bin/python` |

以下 `notebooklm` と書いたら上の CLI を指す。見つからない時は README のインストール手順を案内する。
「CLI が無い」と結論する前に、必ず上のパスの存在を確かめる。

## 境界(確認のルール)

- **確認なしで実行してよい**: `list` / `status` / `use` / `create` / `source list` / `source add` / `source get` / `source fulltext` / `artifact list` / `ask`(保存なし) / `history`(表示のみ) / `language list`
- **実行前に必ずユーザーに確認する**:
  - 削除系: `delete` / `source delete` / `source delete-by-title` / `source clean`
  - 時間がかかる・失敗しうる: `generate *`(目安: 音声10〜20分、動画15〜45分)
  - ファイルを書く: `download *` / `ask --save-as-note` / `history --save`
- 生成・待機は背後実行にする(前景で待たない)

## 認証

1. 動作確認は **必ず `notebooklm list`** で行う(`auth check` は Cookie の形しか見ないので当てにならない)
2. `Authentication expired` / `Redirected to accounts.google.com` が出たら、壊れたのではなくログイン期限切れ
3. ユーザーに「Chrome の窓が開くので Google にログインしてください」と伝え、同じフォルダの `scripts/nlm_login.py` を **venv の Python で背後実行**する
4. ユーザーが「ログインできた」と言ったら、`scripts/` に `nlm_save_signal` という空ファイルを作る → ログイン情報が保存され窓が閉じる
5. `notebooklm list` が一覧を返せば完了

組み込みの `notebooklm login` は Enter 入力を待つ対話型なので、Claude Code からは使わない。
ログイン情報は `~/.notebooklm/storage_state.json` に保存される。**この中身を読んだり画面に出したりしない。**

## クイックリファレンス

| タスク | コマンド |
|---|---|
| ノートブック一覧 | `notebooklm list` (`--json` で機械読み取り) |
| ノートブック作成 | `notebooklm create "タイトル" --use` |
| 操作対象を切り替え/確認 | `notebooklm use <notebook_id>` / `notebooklm status` |
| ノートブック削除 | `notebooklm delete -n <notebook_id>` ⚠確認 |
| 資料を追加(URL/ファイル/YouTube/画像) | `notebooklm source add "https://..."` / `notebooklm source add ./file.pdf` |
| Google ドライブの資料を追加 | `notebooklm source add-drive <file_id>` |
| Web 検索して資料を追加 | `notebooklm source add-research "検索語"` |
| 資料一覧 | `notebooklm source list --json` |
| 資料の処理完了を待つ | `notebooklm source wait <source_id>` |
| 資料を削除 | `notebooklm source delete <source_id>` ⚠確認 |
| 資料を題名で削除 | `notebooklm source delete-by-title "正確な題名"` ⚠確認 |
| 重複・エラー資料を一掃 | `notebooklm source clean` ⚠確認 |
| 資料の名前変更 | `notebooklm source rename <source_id> "新しい名前"` |
| URL 資料を最新化 | `notebooklm source refresh <source_id>` |
| 資料の全文 / 要約 | `notebooklm source fulltext <id>` / `notebooklm source guide <id>` |
| 質問する | `notebooklm ask "質問"` (`-s <source_id>` で資料を限定) |
| 各種生成 | `notebooklm generate audio\|video\|slide-deck\|report\|quiz\|flashcards\|infographic\|mind-map\|data-table` |
| 生成物の一覧 / 完了待ち | `notebooklm artifact list` / `notebooklm artifact wait <artifact_id>` |
| ダウンロード | `notebooklm download <種類> <保存先> --artifact <id>` |
| 出力言語 | `generate` に `--language ja` を付ける |

ID は前方一致で指定できる(`abc` → `abc123...`)。

## 生成タイプ

共通オプション: `-s/--source`(資料を限定) `--language` `--json` `--retry N` `--prompt-file <file>`

| タイプ | コマンド | 主なオプション | 保存形式 |
|---|---|---|---|
| 音声(ポッドキャスト) | `generate audio` | `--format deep-dive\|brief\|critique\|debate` `--length short\|default\|long` | .mp3 |
| 動画 | `generate video` | `--format explainer\|brief` | .mp4 |
| スライド | `generate slide-deck` | `--format detailed\|presenter` `--length default\|short` | .pdf / .pptx |
| インフォグラフィック | `generate infographic` | `--orientation landscape\|portrait\|square` | .png |
| レポート | `generate report` | `--format briefing-doc\|study-guide\|blog-post\|custom` | .md |
| マインドマップ | `generate mind-map` | (即時) | .json |
| データ表 | `generate data-table` | 説明文が必須 | .csv |
| クイズ/単語帳 | `generate quiz` / `generate flashcards` | `--difficulty easy\|medium\|hard` | .json/.md/.html |

スライドを PNG まで書き出したい時は `notebooklm-slides` スキルを使う。
ノートブック名の一括整理は `notebooklm-organize` スキルを使う。

## 典型的な流れ

**資料からポッドキャスト**: `create` → `source add` を資料ごとに → `source list --json` で全部 `ready` を確認 → (確認) `generate audio "〜に焦点を当てて" --language ja` → `artifact wait` → (確認) `download audio ./podcast.mp3`

**資料の入れ替え**: `source list --json` で一覧を見せる → 消す資料をユーザーと確認 → `source delete` → `source add` → `source list` で結果を確かめる

## 結果の確かめ方(必須)

書き込み系コマンドが成功を返しても、**必ず読み取りコマンドで取り直して確かめてから報告する**。
- 追加・削除・名前変更 → `source list --json`
- ノートブック作成・削除 → `list --json`
- 生成 → `artifact list`

## 落とし穴

| 症状 | 原因 | 対処 |
|---|---|---|
| 認証エラー | ログイン期限切れ(約2週間) | 上の「認証」手順 |
| `No notebook context` | 操作対象が未設定 | `notebooklm use <id>` |
| 生成失敗・レート制限 | Google 側の制限 | 5〜10分空けて再実行 |
| ダウンロード失敗 | 生成が未完了 | `artifact list` で状態を確認 |
| ノートブックの `rename` が反映されない | 2026-07 の刷新後の不具合 | `notebooklm-organize` のブラウザ手順 |

非公式 API のため、Google が予告なく仕様を変える可能性がある。
