"""把 classes.dex 注入 aapt2 生成的 APK，再输出新的 APK。

APK 是普通 zip，但 classes.dex 按规范应放在包内靠前位置且不压缩，
这样系统安装时可以直接 mmap 读取，启动也更快。这里保持其它条目的
原始顺序与压缩方式不变，只额外插入 classes.dex。

用法:
    py -I repack.py <in.apk> <classes.dex> <out.apk>
"""

import sys
import zipfile

# 不压缩的扩展名（与 aapt 的行为保持一致）
STORE_EXT = (".png", ".jpg", ".jpeg", ".ogg", ".mp3", ".wav", ".arsc")


def should_store(name):
    return name.lower().endswith(STORE_EXT) or name == "resources.arsc"


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2

    src, dex_path, out = sys.argv[1], sys.argv[2], sys.argv[3]

    with zipfile.ZipFile(src, "r") as zin:
        entries = [(i, zin.read(i.filename)) for i in zin.infolist()]

    with zipfile.ZipFile(out, "w") as zout:
        # classes.dex 放最前面，store 方式
        with open(dex_path, "rb") as f:
            zout.writestr(zipfile.ZipInfo("classes.dex"), f.read(),
                          compress_type=zipfile.ZIP_STORED)

        for info, data in entries:
            name = info.filename
            if name == "classes.dex":
                continue
            ct = zipfile.ZIP_STORED if should_store(name) else zipfile.ZIP_DEFLATED
            zout.writestr(name, data, compress_type=ct)

    print(f"    repacked -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
