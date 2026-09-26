# 原稿ファイルから NotebookLM でスライドを作り、PDF と 1枚ずつの PNG に書き出すまでを1本で回す。
#
# 実行(生成に10〜20分かかるので背後実行にする):
#   python nlm_slides.py --source 原稿.md --out ./slides_out [--ref キャラ1.png --ref キャラ2.png]
#                        [--prompt "指示文" | --prompt-file 指示.txt] [--language ja]
#   既にノートブックがあれば --notebook <ID> で、資料の追加を飛ばして生成だけやり直す
#
# やること: ノートブック作成 → 原稿(+参考画像)を資料に追加 → スライド生成 → 完成待ち
#          → <out>/slides.pdf → <out>/slide_NN.png(幅1280)
# ログインが切れていたら Authentication expired で止まる → notebooklm スキルの nlm_login.py でログインし直す
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

VENV = Path.home() / ".notebooklm-venv"
NLM = VENV / "Scripts" / "notebooklm.exe" if os.name == "nt" else VENV / "bin" / "notebooklm"


def run(*args, timeout=600):
    r = subprocess.run([str(NLM), *map(str, args)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    if r.returncode != 0:
        sys.exit(f"失敗: notebooklm {' '.join(map(str, args))}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="スライドの原稿(md / txt / pdf)")
    ap.add_argument("--out", required=True, help="PDF と PNG の保存先フォルダ")
    ap.add_argument("--ref", action="append", default=[], help="参考画像(キャラ設定画など)。複数可")
    ap.add_argument("--prompt", default=None, help="スライドへの指示文")
    ap.add_argument("--prompt-file", default=None, help="指示文を書いたファイル")
    ap.add_argument("--title", default=None, help="ノートブック名(省略時は原稿のファイル名)")
    ap.add_argument("--language", default="ja")
    ap.add_argument("--notebook", default=None, help="既存ノートブックのID(資料追加を飛ばす)")
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()

    if not NLM.exists():
        sys.exit(f"notebooklm CLI が見つからない: {NLM}(README のインストール手順を参照)")
    src = Path(a.source)
    refs = [Path(r) for r in a.ref]
    for f in [src, *refs] + ([Path(a.prompt_file)] if a.prompt_file else []):
        if not f.exists():
            sys.exit(f"見つからない: {f}")

    if a.notebook:
        nb = a.notebook
        run("use", nb)
    else:
        made = json.loads(run("create", a.title or src.stem, "--use", "--json"))
        made = made.get("notebook", made)
        nb = made.get("id") or made.get("notebook_id")
        if not nb:
            sys.exit(f"ノートブックのIDが読めない: {made}")
        for f in [src, *refs]:
            print(run("source", "add", f, "--timeout", 120).strip())
    print("notebook", nb)

    gen = ["generate", "slide-deck", "--language", a.language, "--json"]
    if a.prompt_file:
        gen += ["--prompt-file", a.prompt_file]
    elif a.prompt:
        gen.insert(2, a.prompt)
    task = json.loads(run(*gen))
    task_id = task.get("task_id") or task.get("id")
    print("生成中", task_id)
    run("artifact", "wait", task_id, "--timeout", a.timeout, timeout=a.timeout + 60)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / "slides.pdf"
    run("download", "slide-deck", pdf, "--artifact", task_id, "--force")

    import fitz  # pymupdf
    from PIL import Image
    doc = fitz.open(pdf)
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=200)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if im.width > 1280:
            im = im.resize((1280, round(im.height * 1280 / im.width)), Image.LANCZOS)
        im.save(out / f"slide_{i:02d}.png")
    print(f"完成: {doc.page_count}枚 -> {out}")


if __name__ == "__main__":
    main()
