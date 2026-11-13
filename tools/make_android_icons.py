"""Generate the Android launcher icons from the same design as the web app.

Android needs a raster icon per density bucket (mdpi..xxxhdpi).  We render the
master at the largest size and downsample, which keeps the small buckets crisp.

Run:  py -I tools/make_android_icons.py
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image  # noqa: E402

from make_icons import draw_icon  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "android", "res")

# 传统 launcher icon：48dp 基准
DENSITIES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}

# adaptive icon 前景层：108dp，安全区 66dp
FG_DENSITIES = {
    "mdpi": 108,
    "hdpi": 162,
    "xhdpi": 216,
    "xxhdpi": 324,
    "xxxhdpi": 432,
}


def ensure(path):
    os.makedirs(path, exist_ok=True)


def write_png(img, path):
    img.save(path, "PNG", optimize=True)
    print(f"{os.path.relpath(path, ROOT):58s} {img.size[0]:>4}px {os.path.getsize(path) // 1024:>4} KB")


def main():
    master = draw_icon(432)                      # 最高密度母版
    round_master = draw_icon(432)

    for bucket, px in DENSITIES.items():
        d = os.path.join(RES, f"mipmap-{bucket}")
        ensure(d)
        write_png(master.resize((px, px), Image.LANCZOS), os.path.join(d, "ic_launcher.png"))
        # 圆形图标：把内容缩到内切圆内
        circ = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        inner = round_master.resize((int(px * 0.88), int(px * 0.88)), Image.LANCZOS)
        off = (px - inner.size[0]) // 2
        circ.alpha_composite(inner, (off, off))
        mask = Image.new("L", (px * 4, px * 4), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(mask).ellipse([0, 0, px * 4 - 1, px * 4 - 1], fill=255)
        mask = mask.resize((px, px), Image.LANCZOS)
        circ.putalpha(mask)
        write_png(circ, os.path.join(d, "ic_launcher_round.png"))

    # adaptive icon 前景层（透明背景，番茄居中且落在 66dp 安全区内）
    for bucket, px in FG_DENSITIES.items():
        d = os.path.join(RES, f"mipmap-{bucket}")
        ensure(d)
        fg = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        art_px = int(px * 0.62)                  # 66/108 ≈ 0.61
        art = draw_icon(432, ring=False).resize((art_px, art_px), Image.LANCZOS)
        off = (px - art_px) // 2
        fg.alpha_composite(art, (off, off))
        write_png(fg, os.path.join(d, "ic_launcher_foreground.png"))

    # 通知栏小图标：纯白剪影
    print("done")


if __name__ == "__main__":
    main()
