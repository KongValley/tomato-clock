package com.tomato.clock;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.os.Build;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.view.View;
import android.view.Window;
import android.view.WindowInsets;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.MimeTypeMap;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * 番茄钟的原生外壳。
 *
 * 界面是 assets/www/ 下的一份静态页面，这里只负责原生能力：
 *   - 边到边全屏，并把系统栏高度让给页面
 *   - 用虚拟 https 域名提供本地资源（这样 localStorage 有正常 origin）
 *   - 专注期间保持屏幕常亮、结束时震动
 *   - 禁掉缩放 / 长按选择 / 外部跳转，让它更像个 App
 */
public class MainActivity extends Activity {

    private static final int BG = 0xFF0B0A09;

    /** 虚拟域名：把 assets 当成一个正常 https 站点，避免 file:// 的存储与安全限制。 */
    private static final String HOST = "tomato.local";
    private static final String BASE_URL = "https://" + HOST + "/";

    private WebView web;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(BG);

        web = new WebView(this);
        web.setBackgroundColor(BG);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        web.setVerticalScrollBarEnabled(false);
        web.setHorizontalScrollBarEnabled(false);
        web.setLongClickable(false);
        web.setHapticFeedbackEnabled(false);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);            // localStorage：设置与统计存这里
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setTextZoom(100);                      // 忽略系统字体缩放，避免布局被撑破
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                if (request.getUrl() == null) return null;
                if (!HOST.equals(request.getUrl().getHost())) return null;
                return serveAsset(request.getUrl().getPath());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                // 只允许留在应用内部，外部链接一律不跳
                return request.getUrl() == null || !HOST.equals(request.getUrl().getHost());
            }

            @Override
            @SuppressWarnings("deprecation")
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return url == null || !url.startsWith(BASE_URL);
            }
        });

        web.addJavascriptInterface(new Bridge(), "TomatoNative");

        root.addView(web, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT));

        setContentView(root);
        applyEdgeToEdge(root);
        web.loadUrl(BASE_URL + "index.html");
    }

    /** 把 assets/www 下的文件当作 https 响应返回。 */
    private WebResourceResponse serveAsset(String path) {
        if (path == null || path.isEmpty() || "/".equals(path)) path = "/index.html";

        String assetPath = "www" + path;
        String ext = MimeTypeMap.getFileExtensionFromUrl(path).toLowerCase();
        String mime;
        switch (ext) {
            case "html": mime = "text/html"; break;
            case "js":   mime = "application/javascript"; break;
            case "css":  mime = "text/css"; break;
            case "json":
            case "webmanifest": mime = "application/manifest+json"; break;
            case "png":  mime = "image/png"; break;
            case "svg":  mime = "image/svg+xml"; break;
            case "woff2": mime = "font/woff2"; break;
            case "woff": mime = "font/woff"; break;
            default:     mime = "application/octet-stream";
        }

        try {
            InputStream in = getAssets().open(assetPath);
            WebResourceResponse res = new WebResourceResponse(mime, "utf-8", in);
            Map<String, String> headers = new HashMap<>();
            headers.put("Cache-Control", "no-store");
            res.setResponseHeaders(headers);
            return res;
        } catch (IOException e) {
            return new WebResourceResponse("text/plain", "utf-8", 404, "Not Found",
                    new HashMap<String, String>(),
                    new ByteArrayInputStream(new byte[0]));
        }
    }

    /** 让内容延伸到状态栏 / 导航栏下面，再把系统栏高度让给页面。 */
    private void applyEdgeToEdge(final View root) {
        Window w = getWindow();

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            w.setDecorFitsSystemWindows(false);
        } else {
            w.getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
        }

        root.setOnApplyWindowInsetsListener((v, insets) -> {
            int top, bottom, left, right;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                android.graphics.Insets bars = insets.getInsets(
                        WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                top = bars.top;
                bottom = bars.bottom;
                left = bars.left;
                right = bars.right;
            } else {
                top = insets.getSystemWindowInsetTop();
                bottom = insets.getSystemWindowInsetBottom();
                left = insets.getSystemWindowInsetLeft();
                right = insets.getSystemWindowInsetRight();
            }
            // 内边距加在外层容器，WebView 填满剩余区域
            v.setPadding(left, top, right, bottom);
            return insets;
        });
    }

    /** 暴露给页面脚本的原生能力。 */
    private class Bridge {
        @JavascriptInterface
        public void keepAwake(final boolean on) {
            runOnUiThread(() -> {
                if (on) {
                    getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                } else {
                    getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                }
            });
        }

        /** 结束提醒的震动。pattern 形如 "90,60,90"（毫秒，偶数位是间隔）。 */
        @JavascriptInterface
        public void vibrate(final String pattern) {
            try {
                Vibrator v = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
                if (v == null || !v.hasVibrator()) return;

                String[] parts = pattern.split(",");
                long[] timings = new long[parts.length];
                for (int i = 0; i < parts.length; i++) {
                    timings[i] = Long.parseLong(parts[i].trim());
                }
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    v.vibrate(VibrationEffect.createWaveform(timings, -1));
                } else {
                    v.vibrate(timings, -1);
                }
            } catch (Exception ignored) {
                // 震动失败不应该影响计时
            }
        }

        /** 页面据此判断自己运行在原生壳里，从而跳过 Service Worker。 */
        @JavascriptInterface
        public boolean isNative() {
            return true;
        }

        @JavascriptInterface
        public int sdkInt() {
            return Build.VERSION.SDK_INT;
        }
    }

    @Override
    public void onBackPressed() {
        // 单页应用，返回键直接退到桌面
        moveTaskToBack(true);
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override
    protected void onPause() {
        if (web != null) web.onPause();
        super.onPause();
    }
}
