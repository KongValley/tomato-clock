#!/usr/bin/env bash
#
# 构建番茄钟的 Android APK —— 不依赖 Gradle。
#
# 流程：aapt2 compile → aapt2 link → javac → d8 → 注入 dex → zipalign → apksigner
#
# 用法:
#   bash android/build.sh
#
# 环境变量（都有默认值）:
#   JAVA_HOME            JDK 17 目录       默认 E:/dev/jdk/jdk17
#   ANDROID_SDK          Android SDK 目录   默认 E:/dev/android-sdk
#   BUILD_TOOLS_VERSION  默认 34.0.0
#   PLATFORM             默认 android-35
#
# 输出: dist/tomato-clock-<version>.apk

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJ="$(cd "$HERE/.." && pwd)"

JAVA_HOME="${JAVA_HOME:-/e/dev/jdk/jdk17}"
ANDROID_SDK="${ANDROID_SDK:-/e/dev/android-sdk}"

BUILD_TOOLS_VERSION="${BUILD_TOOLS_VERSION:-34.0.0}"
PLATFORM="${PLATFORM:-android-35}"

BT="$ANDROID_SDK/build-tools/$BUILD_TOOLS_VERSION"
ANDROID_JAR="$ANDROID_SDK/platforms/$PLATFORM/android.jar"

VERSION_NAME="1.0"
VERSION_CODE="1"
APK_NAME="tomato-clock-${VERSION_NAME}.apk"

fail() { echo "错误: $*" >&2; exit 1; }

# ---------- 工具发现 ----------
[ -x "$JAVA_HOME/bin/javac.exe" ] || [ -x "$JAVA_HOME/bin/javac" ] \
  || fail "找不到 JDK：$JAVA_HOME"
[ -d "$BT" ] || fail "找不到 build-tools：$BT"
[ -f "$ANDROID_JAR" ] || fail "找不到 android.jar：$ANDROID_JAR"

export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"

AAPT2="$BT/aapt2.exe";         [ -x "$AAPT2" ] || AAPT2="$BT/aapt2"
ZIPALIGN="$BT/zipalign.exe";   [ -x "$ZIPALIGN" ] || ZIPALIGN="$BT/zipalign"
D8="$BT/d8.bat";               [ -f "$D8" ] || D8="$BT/d8"
APKSIGNER="$BT/apksigner.bat"; [ -f "$APKSIGNER" ] || APKSIGNER="$BT/apksigner"

# 原生 Windows 工具（javac / d8）不认 /f/... 的 MSYS 路径，统一转换
winpath() {
  if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi
}

WORK="$PROJ/android/build"
DIST="$PROJ/dist"

rm -rf "$WORK"
mkdir -p "$WORK"/{res,gen,classes,dex,assets/www} "$DIST"

echo "==> 1/7 拷贝网页资源到 assets/www"
# APK 里不需要 Service Worker：资源直接来自本地包，离线天然成立
cp "$PROJ/index.html" "$WORK/assets/www/"
cp "$PROJ/manifest.webmanifest" "$WORK/assets/www/"
mkdir -p "$WORK/assets/www/icons"
# og.png 只用于社交分享预览，不必打进 App
for icon in "$PROJ"/icons/*.png; do
  [ "$(basename "$icon")" = "og.png" ] && continue
  cp "$icon" "$WORK/assets/www/icons/"
done
# 内嵌字体
if [ -d "$PROJ/fonts" ]; then
  mkdir -p "$WORK/assets/www/fonts"
  cp "$PROJ"/fonts/*.woff2 "$WORK/assets/www/fonts/"
fi

echo "==> 2/7 编译资源 (aapt2 compile)"
"$AAPT2" compile --dir "$PROJ/android/res" -o "$WORK/res/resources.zip"

echo "==> 3/7 链接资源并生成 R.java (aapt2 link)"
"$AAPT2" link \
  -o "$WORK/app-unsigned.apk" \
  -I "$ANDROID_JAR" \
  --manifest "$PROJ/android/AndroidManifest.xml" \
  --java "$WORK/gen" \
  --min-sdk-version 24 \
  --target-sdk-version 35 \
  --version-code "$VERSION_CODE" \
  --version-name "$VERSION_NAME" \
  --auto-add-overlay \
  -A "$WORK/assets" \
  "$WORK/res/resources.zip"

echo "==> 4/7 编译 Java 源码 (javac)"
# @file 内必须是 Windows 路径，否则 javac 报"找不到文件"
: > "$WORK/sources.txt"
while IFS= read -r f; do winpath "$f" >> "$WORK/sources.txt"; done < <(
  find "$PROJ/android/src" "$WORK/gen" -name '*.java'
)

# JDK 17 不允许 -source/-target 11 配 -bootclasspath，
# 用 --release 11 + classpath 指向 android.jar（标准 Android 做法）
if ! javac -encoding UTF-8 --release 11 \
      -classpath "$(winpath "$ANDROID_JAR")" \
      -d "$(winpath "$WORK/classes")" \
      @"$(winpath "$WORK/sources.txt")" > "$WORK/javac.log" 2>&1; then
  cat "$WORK/javac.log" >&2
  fail "javac 编译失败"
fi
grep -vE "^(注|Note|警告|warning):" "$WORK/javac.log" || true

CLASS_COUNT=$(find "$WORK/classes" -name '*.class' | wc -l)
[ "$CLASS_COUNT" -gt 0 ] || fail "javac 没有产出 class 文件"
echo "    $CLASS_COUNT 个 class"

echo "==> 5/7 转成 dex (d8)"
: > "$WORK/classes.txt"
while IFS= read -r f; do winpath "$f" >> "$WORK/classes.txt"; done < <(
  find "$WORK/classes" -name '*.class'
)
"$D8" --release --min-api 24 \
  --lib "$(winpath "$ANDROID_JAR")" \
  --output "$(winpath "$WORK/dex")" \
  @"$(winpath "$WORK/classes.txt")"
[ -f "$WORK/dex/classes.dex" ] || fail "d8 没有产出 classes.dex"

echo "==> 6/7 注入 classes.dex"
py -I "$HERE/repack.py" "$WORK/app-unsigned.apk" "$WORK/dex/classes.dex" "$WORK/app-with-dex.apk"

echo "==> 7/7 对齐并签名 (zipalign + apksigner)"
"$ZIPALIGN" -f -p 4 "$WORK/app-with-dex.apk" "$WORK/app-aligned.apk"

KEYSTORE="${TOMATO_KEYSTORE:-$PROJ/android/signing/tomato.keystore}"
KEY_ALIAS="${TOMATO_KEY_ALIAS:-tomato}"
# 密钥库口令：优先用环境变量；否则读 signing/ 下的口令文件；都没有则随机生成。
# 不把口令写死在脚本里——仓库是公开的。
PASS_FILE="$PROJ/android/signing/password.txt"

if [ -z "${TOMATO_KS_PASS:-}" ] && [ -f "$PASS_FILE" ]; then
  TOMATO_KS_PASS="$(cat "$PASS_FILE")"
fi

if [ -z "${TOMATO_KS_PASS:-}" ]; then
  if [ -f "$KEYSTORE" ]; then
    fail "密钥库已存在但找不到口令：请设置 TOMATO_KS_PASS，或把口令写入 $PASS_FILE"
  fi
  TOMATO_KS_PASS="$(head -c 24 /dev/urandom | od -An -tx1 | tr -d ' \n')"
  mkdir -p "$(dirname "$PASS_FILE")"
  printf '%s' "$TOMATO_KS_PASS" > "$PASS_FILE"
  echo "    已生成随机密钥库口令，保存在 android/signing/password.txt（不会提交）"
fi

KS_PASS="$TOMATO_KS_PASS"
KEY_PASS="${TOMATO_KEY_PASS:-$TOMATO_KS_PASS}"

if [ ! -f "$KEYSTORE" ]; then
  echo "    未找到密钥库，生成自签名密钥"
  mkdir -p "$(dirname "$KEYSTORE")"
  keytool -genkeypair \
    -keystore "$(winpath "$KEYSTORE")" \
    -alias "$KEY_ALIAS" \
    -keyalg RSA -keysize 2048 -validity 10950 \
    -storepass "$KS_PASS" -keypass "$KEY_PASS" \
    -dname "CN=Tomato Clock, OU=Personal, O=Tomato, C=CN" >/dev/null 2>&1
fi

# 同时启用 v1/v2/v3：minSdk 24 需要 v1 才能在 Android 7.x 上安装
"$APKSIGNER" sign \
  --ks "$(winpath "$KEYSTORE")" \
  --ks-key-alias "$KEY_ALIAS" \
  --ks-pass "pass:$KS_PASS" \
  --key-pass "pass:$KEY_PASS" \
  --v1-signing-enabled true \
  --v2-signing-enabled true \
  --v3-signing-enabled true \
  --out "$DIST/$APK_NAME" \
  "$WORK/app-aligned.apk"

"$APKSIGNER" verify --print-certs "$DIST/$APK_NAME" | head -5
"$APKSIGNER" verify --verbose "$DIST/$APK_NAME" | grep -E "^Verified" | head -4

SIZE=$(du -h "$DIST/$APK_NAME" | cut -f1)
echo
echo "✓ 构建完成: dist/$APK_NAME ($SIZE)"
