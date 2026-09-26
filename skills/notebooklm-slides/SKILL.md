---
name: notebooklm-slides
description: 原稿ファイル(md / txt / pdf)から NotebookLM でスライドを生成し、PDF と 1枚ずつの PNG に書き出すスキル。キャラクター設定画などの参考画像も資料に添えて、絵柄をそろえたスライドを作れる。発火トリガー: 「NotebookLMでスライドを作って」「この原稿をスライドにして」「スライドをPNGで書き出して」「キャラ固定のスライド」「/notebooklm-slides」。
---

# NotebookLM スライド生成

目的: 原稿1本から、そのまま記事や資料に貼れるスライド画像を作る。
成果物: 保存先フォルダに `slides.pdf` と `slide_01.png` 〜 が並び、枚数を報告した状態。

## 前提

- `notebooklm` スキルの CLI が入っていて、`notebooklm list` が通ること(通らなければ `notebooklm` スキルの「認証」手順)
- venv に `pymupdf` と `pillow` が入っていること(README のインストール手順に含まれる)

## 進め方

1. ユーザーに次を確認する(分かっているものは聞かない)
   - 原稿ファイルの場所
   - 保存先フォルダ(省略時は原稿と同じ場所の `slides_out`)
   - 参考画像(キャラ設定画・ロゴ等)があるか
   - スライドへの指示(例: 「1枚1メッセージ、図を多めに」)
2. 生成に10〜20分かかることを伝えてから、`scripts/nlm_slides.py` を **venv の Python で背後実行**する

   ```
   python nlm_slides.py --source <原稿> --out <保存先> [--ref <画像>]... [--prompt "<指示>"] --language ja
   ```

   指示が長い時は `--prompt-file <指示.txt>` を使う。
3. 終わったら保存先の PNG の枚数を数えて報告し、保存先フォルダを開いて見せる

## やり直し

生成結果には当たり外れがある。2本目を作る時は、表示された notebook ID を使って資料追加を飛ばす。

```
python nlm_slides.py --source <原稿> --out <別の保存先> --notebook <ID> --prompt "<直したい点>"
```

## 落とし穴

| 症状 | 対処 |
|---|---|
| `Authentication expired` で止まる | `notebooklm` スキルの `nlm_login.py` でログインし直す |
| 生成がタイムアウトする | `--timeout 2700` に延ばす。Google 側の混雑時は時間を空ける |
| 絵柄が参考画像に似ない | 指示文に「資料の画像のキャラクターを全スライドで使う」と明記する |
