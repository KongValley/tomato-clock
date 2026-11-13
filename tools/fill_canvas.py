"""把无限画布模板填充成「番茄钟」项目的设计交付。

用法: py -I 原型/_fill_canvas.py
"""

import io

PATH = "原型/番茄钟-无限画布.html"

# ---------- 页面 HTML 片段（Row 3，全部使用原型同一套 token） ----------
PAGE_BASE = """
<style>
  .pg{{position:relative;width:100%;height:100%;background:#0D0C0A;color:#F2EDE6;
      font-family:"PingFang SC","Microsoft YaHei UI","Microsoft YaHei",system-ui,sans-serif;
      display:flex;flex-direction:column;overflow:hidden;}}
  .pg *{{box-sizing:border-box;margin:0;padding:0}}
  .pg-top{{flex:none;display:flex;align-items:center;justify-content:space-between;
      height:52px;padding:0 20px;border-bottom:1px solid rgba(242,237,230,.07)}}
  .pg-brand{{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:600}}
  .pg-body{{flex:1;min-height:0;display:flex;flex-direction:column;padding:0 20px}}
  .pg-num{{font-family:"Bahnschrift","Segoe UI Variable Display",sans-serif;font-variant-numeric:tabular-nums}}
</style>
"""


def page_timer():
    """计时页 390x844"""
    pips = "".join(
        f'<span style="width:22px;height:3px;background:{"#E2552F" if i < 1 else "rgba(242,237,230,.13)"}"></span>'
        for i in range(4)
    )
    ticks = ""
    import math
    for i in range(60):
        major = i % 5 == 0
        a = (i / 60) * math.pi * 2 - math.pi / 2
        r1, r2 = 141, (128 if major else 134)
        x1, y1 = 150 + math.cos(a) * r1, 150 + math.sin(a) * r1
        x2, y2 = 150 + math.cos(a) * r2, 150 + math.sin(a) * r2
        ticks += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                  f'stroke="rgba(242,237,230,{".22" if major else ".13"})" '
                  f'stroke-width="{2 if major else 1.5}"/>')
    return PAGE_BASE + f"""
<div class="pg">
  <div class="pg-top">
    <div class="pg-brand">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#E2552F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 21c4.4 0 7.5-3 7.5-7.1 0-4-3.1-6.9-7.5-6.9s-7.5 2.9-7.5 6.9C4.5 18 7.6 21 12 21Z"/>
        <path d="M12 7V4.2"/><path d="M12 5.4c-1.3-1-2.9-1.3-4.3-.8M12 5.4c1.3-1 2.9-1.3 4.3-.8"/>
      </svg>
      番茄钟
    </div>
    <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="rgba(242,237,230,.42)" stroke-width="1.6" stroke-linecap="round">
      <circle cx="12" cy="12" r="2.8"/>
      <path d="M12 3.2v2.1M12 18.7v2.1M4.6 7.8l1.8 1.1M17.6 15.1l1.8 1.1M4.6 16.2l1.8-1.1M17.6 8.9l1.8-1.1"/>
    </svg>
  </div>

  <div class="pg-body">
    <div style="margin-top:20px;display:flex;align-items:center;gap:12px;padding:12px 16px;
                border:1px solid rgba(242,237,230,.07);border-radius:6px;background:#14120F;">
      <div style="flex:1;min-width:0">
        <div style="font-size:10.5px;font-weight:600;letter-spacing:.16em;color:#8A8078;text-transform:uppercase">本轮专注</div>
        <div style="margin-top:2px;font-size:15px;font-weight:600">写完方案第 2 节</div>
      </div>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(242,237,230,.42)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9.4 5.6 16 12l-6.6 6.4"/>
      </svg>
    </div>

    <div style="position:relative;flex:1;display:grid;place-items:center;margin-top:16px">
      <div style="position:relative;width:300px;height:300px">
        <svg viewBox="0 0 300 300" style="width:100%;height:100%;display:block">
          {ticks}
          <circle cx="150" cy="150" r="118" fill="none" stroke="rgba(242,237,230,.07)" stroke-width="2.5"/>
          <circle cx="150" cy="150" r="118" fill="none" stroke="#E2552F" stroke-width="2.5"
                  stroke-linecap="round" stroke-dasharray="741.42" stroke-dashoffset="690"
                  transform="rotate(-90 150 150)"/>
          <g transform="translate(159.5 40.5)">
            <path d="M0 -7 L3.4 -1.2 L0 4.6 L-3.4 -1.2 Z" fill="#E2552F"/>
          </g>
        </svg>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
          <div style="font-size:11px;font-weight:600;letter-spacing:.2em;color:#E2552F;text-indent:.2em">专注</div>
          <div class="pg-num" style="margin-top:8px;font-size:68px;font-weight:300;line-height:1;letter-spacing:-.02em">25:00</div>
          <div style="margin-top:12px;font-size:12px;color:#A79C8F">第 1 个番茄</div>
        </div>
      </div>
    </div>

    <div style="display:flex;align-items:center;gap:12px;margin-top:12px">
      <div style="display:flex;gap:5px">{pips}</div>
      <span style="font-size:12px;color:#A79C8F">本轮 1 / 4</span>
    </div>

    <div style="display:grid;grid-template-columns:48px 68px 48px;justify-content:center;align-items:center;gap:32px;margin-top:24px">
      <div style="width:48px;height:48px;border-radius:999px;border:1px solid rgba(242,237,230,.07);display:grid;place-items:center">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="rgba(242,237,230,.32)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3.6 11.2a8.4 8.4 0 1 0 3-6.4"/><path d="M3.6 4.6v5.1h5.1"/>
        </svg>
      </div>
      <div style="width:68px;height:68px;border-radius:999px;background:#E2552F;display:grid;place-items:center">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="#170904"><path d="M8.4 5.6c0-.85.93-1.36 1.65-.9l8.2 5.4a1.06 1.06 0 0 1 0 1.8l-8.2 5.4c-.72.46-1.65-.05-1.65-.9Z"/></svg>
      </div>
      <div style="width:48px;height:48px;border-radius:999px;border:1px solid rgba(242,237,230,.07);display:grid;place-items:center">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="rgba(242,237,230,.32)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 5.6c0-.85.93-1.36 1.65-.9l7.3 5.2a1.06 1.06 0 0 1 0 1.8l-7.3 5.2c-.72.46-1.65-.05-1.65-.9Z"/><path d="M17.6 5.2v13.6"/>
        </svg>
      </div>
    </div>

    <div style="display:flex;align-items:center;gap:16px;margin-top:24px;padding-top:16px;
                border-top:1px solid rgba(242,237,230,.07);font-size:12px;color:#8A8078">
      <span>今日 <b style="color:#F2EDE6">1</b> 个番茄</span>
      <span style="width:1px;height:11px;background:rgba(242,237,230,.13)"></span>
      <span>专注 <b style="color:#F2EDE6">25</b> 分钟</span>
      <span style="width:1px;height:11px;background:rgba(242,237,230,.13)"></span>
      <span>连续 <b style="color:#F2EDE6">4</b> 天</span>
    </div>
  </div>

  <div style="flex:none;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid rgba(242,237,230,.07)">
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#F2EDE6;position:relative">
      <span style="position:absolute;top:-1px;left:50%;transform:translateX(-50%);width:24px;height:2px;background:#E2552F"></span>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#E2552F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="13.4" r="7.4"/><path d="M12 9.6v3.8l2.3 1.6"/><path d="M9.3 2.8h5.4"/>
      </svg>计时
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#8A8078">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4.5 7.2 6 8.7l2.4-2.7M4.5 12.4 6 13.9l2.4-2.7M4.5 17.6 6 19.1l2.4-2.7"/><path d="M11.6 7.8h8M11.6 13h8M11.6 18.2h5.4"/>
      </svg>任务
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#8A8078">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3.4 20.2h17.2"/><path d="M7 20.2v-6.4M12 20.2V8M17 20.2v-4.2"/>
      </svg>记录
    </div>
  </div>
</div>
"""


def page_tasks():
    rows = [
        ("写完方案第 2 节", 2, 4, True),
        ("整理上周会议记录", 1, 2, False),
        ("回复设计评审意见", 0, 3, False),
    ]
    html_rows = ""
    for name, done, est, cur in rows:
        pips = "".join(
            f'<i style="display:block;width:2px;height:9px;background:{"#E2552F" if i < done else "rgba(242,237,230,.22)"}"></i>'
            for i in range(est)
        )
        cur_badge = ('<span style="align-self:center;padding:3px 7px;font-size:10px;font-weight:600;'
                     'letter-spacing:.1em;color:#E2552F;border:1px solid currentColor;border-radius:2px">当前</span>'
                     if cur else "")
        html_rows += f"""
    <div style="display:flex;align-items:stretch;border-bottom:1px solid rgba(242,237,230,.07);padding:13px 0">
      <div style="flex:1;display:flex;align-items:center;gap:12px;min-width:0">
        <span style="flex:none;width:17px;height:17px;border:1px solid rgba(242,237,230,.22);border-radius:2px"></span>
        <span style="flex:1;min-width:0">
          <span style="display:block;font-size:14.5px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</span>
          <span style="display:flex;align-items:center;gap:8px;margin-top:3px;font-size:11.5px;color:#8A8078">
            <span style="display:inline-flex;gap:3px">{pips}</span>
            {done} / {est} 个番茄
          </span>
        </span>
      </div>
      {cur_badge}
    </div>"""

    done_rows = ""
    for name, done, est in [("备份项目资料", 2, 2), ("更新需求文档目录", 1, 1)]:
        pips = "".join('<i style="display:block;width:2px;height:9px;background:#8A8078"></i>' for _ in range(est))
        done_rows += f"""
    <div style="display:flex;align-items:center;gap:12px;border-bottom:1px solid rgba(242,237,230,.07);padding:13px 0">
      <span style="flex:none;width:17px;height:17px;background:#E2552F;border-radius:2px;display:grid;place-items:center">
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#170904" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5 9.6 17 19 7.4"/></svg>
      </span>
      <span style="flex:1;min-width:0">
        <span style="display:block;font-size:14.5px;font-weight:500;color:#8A8078;text-decoration:line-through">{name}</span>
        <span style="display:flex;align-items:center;gap:8px;margin-top:3px;font-size:11.5px;color:#8A8078">
          <span style="display:inline-flex;gap:3px">{pips}</span>
          {done} / {est} 个番茄
        </span>
      </span>
    </div>"""

    return PAGE_BASE + f"""
<div class="pg">
  <div class="pg-top">
    <div class="pg-brand">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#E2552F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 21c4.4 0 7.5-3 7.5-7.1 0-4-3.1-6.9-7.5-6.9s-7.5 2.9-7.5 6.9C4.5 18 7.6 21 12 21Z"/>
        <path d="M12 7V4.2"/><path d="M12 5.4c-1.3-1-2.9-1.3-4.3-.8M12 5.4c1.3-1 2.9-1.3 4.3-.8"/>
      </svg>
      番茄钟
    </div>
    <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="rgba(242,237,230,.42)" stroke-width="1.6" stroke-linecap="round">
      <circle cx="12" cy="12" r="2.8"/>
      <path d="M12 3.2v2.1M12 18.7v2.1M4.6 7.8l1.8 1.1M17.6 15.1l1.8 1.1M4.6 16.2l1.8-1.1M17.6 8.9l1.8-1.1"/>
    </svg>
  </div>

  <div class="pg-body" style="padding-bottom:0">
    <div style="display:flex;align-items:center;justify-content:space-between;padding:24px 0 20px">
      <h1 style="font-size:24px;font-weight:600;letter-spacing:-.01em">任务</h1>
      <span style="display:inline-flex;align-items:center;gap:6px;padding:7px 11px 7px 9px;
                   font-size:13px;font-weight:600;border:1px solid rgba(242,237,230,.13);border-radius:6px">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#E2552F" stroke-width="1.9" stroke-linecap="round"><path d="M12 5.4v13.2M5.4 12h13.2"/></svg>
        新建
      </span>
    </div>

    <div style="display:flex;justify-content:space-between;padding-bottom:8px;
                font-size:10.5px;font-weight:600;letter-spacing:.16em;color:#8A8078;text-transform:uppercase">
      <span>进行中</span><span>3</span>
    </div>
    {html_rows}

    <div style="display:flex;justify-content:space-between;padding:28px 0 8px;
                font-size:10.5px;font-weight:600;letter-spacing:.16em;color:#8A8078;text-transform:uppercase">
      <span>已完成</span><span>2</span>
    </div>
    {done_rows}
  </div>

  <div style="flex:none;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid rgba(242,237,230,.07)">
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#8A8078">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="13.4" r="7.4"/><path d="M12 9.6v3.8l2.3 1.6"/><path d="M9.3 2.8h5.4"/>
      </svg>计时
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#F2EDE6;position:relative">
      <span style="position:absolute;top:-1px;left:50%;transform:translateX(-50%);width:24px;height:2px;background:#E2552F"></span>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#E2552F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4.5 7.2 6 8.7l2.4-2.7M4.5 12.4 6 13.9l2.4-2.7M4.5 17.6 6 19.1l2.4-2.7"/><path d="M11.6 7.8h8M11.6 13h8M11.6 18.2h5.4"/>
      </svg>任务
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#8A8078">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3.4 20.2h17.2"/><path d="M7 20.2v-6.4M12 20.2V8M17 20.2v-4.2"/>
      </svg>记录
    </div>
  </div>
</div>
"""


def page_stats():
    bars = [("周四", 3), ("周五", 5), ("周六", 2), ("周日", 0), ("周一", 6), ("周二", 4), ("今天", 1)]
    maxv = 6
    chart = ""
    W, H, padB, padT = 320, 132, 22, 14
    plotH = H - padB - padT
    slot = W / len(bars)
    barW = round(slot * 0.52)
    chart += f'<line x1="0" y1="{H-padB}" x2="{W}" y2="{H-padB}" stroke="rgba(242,237,230,.13)" stroke-width="1"/>'
    for i, (label, v) in enumerate(bars):
        x = i * slot + (slot - barW) / 2
        if v > 0:
            h = v / maxv * plotH
            y = H - padB - h
            fill = "#E2552F" if label == "今天" else "#4A443C"
            chart += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{barW}" height="{h:.1f}" rx="1" fill="{fill}"/>'
                      f'<text x="{x+barW/2:.1f}" y="{max(9, y-6):.1f}" fill="#A79C8F" font-size="9.5" '
                      f'text-anchor="middle" font-family="Bahnschrift,sans-serif">{v}</text>')
        chart += (f'<text x="{x+barW/2:.1f}" y="{H-6}" fill="{"#F2EDE6" if label=="今天" else "#8A8078"}" '
                  f'font-size="10" text-anchor="middle" font-weight="{600 if label=="今天" else 400}">{label}</text>')

    ruler = "".join(
        f'<i style="flex:1;max-width:8px;height:{26 if i==13 else 18}px;'
        f'background:{"#E2552F" if i >= 10 else "rgba(242,237,230,.13)"};border-radius:1px"></i>'
        for i in range(14)
    )

    return PAGE_BASE + f"""
<div class="pg">
  <div class="pg-top">
    <div class="pg-brand">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#E2552F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 21c4.4 0 7.5-3 7.5-7.1 0-4-3.1-6.9-7.5-6.9s-7.5 2.9-7.5 6.9C4.5 18 7.6 21 12 21Z"/>
        <path d="M12 7V4.2"/><path d="M12 5.4c-1.3-1-2.9-1.3-4.3-.8M12 5.4c1.3-1 2.9-1.3 4.3-.8"/>
      </svg>
      番茄钟
    </div>
    <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="rgba(242,237,230,.42)" stroke-width="1.6" stroke-linecap="round">
      <circle cx="12" cy="12" r="2.8"/>
      <path d="M12 3.2v2.1M12 18.7v2.1M4.6 7.8l1.8 1.1M17.6 15.1l1.8 1.1M4.6 16.2l1.8-1.1M17.6 8.9l1.8-1.1"/>
    </svg>
  </div>

  <div class="pg-body" style="padding-bottom:0">
    <div style="display:flex;align-items:center;justify-content:space-between;padding:24px 0 20px">
      <h1 style="font-size:24px;font-weight:600;letter-spacing:-.01em">记录</h1>
      <span style="padding:3px 7px;font-size:10.5px;color:#8A8078;border:1px dashed rgba(242,237,230,.13);border-radius:2px">示例数据</span>
    </div>

    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(242,237,230,.07);
                border-top:1px solid rgba(242,237,230,.07);border-bottom:1px solid rgba(242,237,230,.07)">
      <div style="background:#0D0C0A;padding:16px 0 16px 4px">
        <b class="pg-num" style="display:block;font-size:30px;font-weight:400;line-height:1.05">1</b>
        <span style="display:block;margin-top:5px;font-size:11.5px;color:#8A8078">今日番茄</span>
      </div>
      <div style="background:#0D0C0A;padding:16px 0 16px 4px">
        <b class="pg-num" style="display:block;font-size:30px;font-weight:400;line-height:1.05">25</b>
        <span style="display:block;margin-top:5px;font-size:11.5px;color:#8A8078">今日分钟</span>
      </div>
      <div style="background:#0D0C0A;padding:16px 0 16px 4px">
        <b class="pg-num" style="display:block;font-size:30px;font-weight:400;line-height:1.05">50%</b>
        <span style="display:block;margin-top:5px;font-size:11.5px;color:#8A8078">计划完成</span>
      </div>
    </div>

    <div style="display:flex;align-items:baseline;justify-content:space-between;padding:28px 0 16px">
      <span style="font-size:13px;font-weight:600">最近七天</span>
      <span style="font-size:11.5px;color:#8A8078">21 个番茄</span>
    </div>
    <svg viewBox="0 0 320 132" style="width:100%;height:132px;display:block">{chart}</svg>

    <div style="display:flex;align-items:baseline;justify-content:space-between;padding:28px 0 16px">
      <span style="font-size:13px;font-weight:600">连续专注</span>
    </div>
    <div style="display:flex;align-items:center;gap:16px;padding:20px 0 16px;border-top:1px solid rgba(242,237,230,.07)">
      <div style="flex:none;display:flex;align-items:baseline;gap:8px">
        <span class="pg-num" style="font-size:26px;font-weight:400;line-height:1">4</span>
        <span style="font-size:12px;color:#8A8078">天</span>
      </div>
      <span style="font-size:12px;color:#8A8078;line-height:1.4">连续达成<br>近 14 天</span>
      <div style="flex:1;display:flex;gap:3px;justify-content:flex-end;align-items:flex-end">{ruler}</div>
    </div>
  </div>

  <div style="flex:none;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid rgba(242,237,230,.07)">
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#8A8078">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="13.4" r="7.4"/><path d="M12 9.6v3.8l2.3 1.6"/><path d="M9.3 2.8h5.4"/>
      </svg>计时
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#8A8078">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4.5 7.2 6 8.7l2.4-2.7M4.5 12.4 6 13.9l2.4-2.7M4.5 17.6 6 19.1l2.4-2.7"/><path d="M11.6 7.8h8M11.6 13h8M11.6 18.2h5.4"/>
      </svg>任务
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:12px 0;font-size:11px;color:#F2EDE6;position:relative">
      <span style="position:absolute;top:-1px;left:50%;transform:translateX(-50%);width:24px;height:2px;background:#E2552F"></span>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#E2552F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3.4 20.2h17.2"/><path d="M7 20.2v-6.4M12 20.2V8M17 20.2v-4.2"/>
      </svg>记录
    </div>
  </div>
</div>
"""


def page_settings():
    def row(label, hint, value, unit):
        return f"""
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;
                padding:13px 0;border-bottom:1px solid rgba(242,237,230,.07)">
      <div>
        <div style="font-size:14px;font-weight:500">{label}</div>
        <div style="margin-top:2px;font-size:11.5px;color:#8A8078">{hint}</div>
      </div>
      <div style="display:flex;align-items:center;gap:1px">
        <span style="display:grid;place-items:center;width:32px;height:32px;border:1px solid rgba(242,237,230,.07);border-radius:2px">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#A79C8F" stroke-width="1.9" stroke-linecap="round"><path d="M5.4 12h13.2"/></svg>
        </span>
        <span class="pg-num" style="min-width:62px;text-align:center;font-size:14px">{value}<span style="font-family:inherit;font-size:11px;color:#8A8078;margin-left:3px">{unit}</span></span>
        <span style="display:grid;place-items:center;width:32px;height:32px;border:1px solid rgba(242,237,230,.07);border-radius:2px">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#A79C8F" stroke-width="1.9" stroke-linecap="round"><path d="M12 5.4v13.2M5.4 12h13.2"/></svg>
        </span>
      </div>
    </div>"""

    def sw(on):
        rail_bg = "#E2552F" if on else "#221F1A"
        knob = "#170904" if on else "#8A8078"
        tr = "translateX(18px)" if on else "none"
        return f"""
      <span style="position:relative;display:block;width:42px;height:24px;flex:none">
        <span style="position:absolute;inset:0;background:{rail_bg};border:1px solid {"#E2552F" if on else "rgba(242,237,230,.13)"};border-radius:2px"></span>
        <span style="position:absolute;top:3px;left:3px;width:16px;height:16px;background:{knob};border-radius:1px;transform:{tr}"></span>
      </span>"""

    def srow(label, hint, on):
        return f"""
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;
                padding:13px 0;border-bottom:1px solid rgba(242,237,230,.07)">
      <div>
        <div style="font-size:14px;font-weight:500">{label}</div>
        <div style="margin-top:2px;font-size:11.5px;color:#8A8078">{hint}</div>
      </div>
      {sw(on)}
    </div>"""

    def group(t):
        return (f'<div style="padding:20px 0 8px;font-size:10.5px;font-weight:600;letter-spacing:.16em;'
                f'text-transform:uppercase;color:#8A8078">{t}</div>')

    return PAGE_BASE + f"""
<div class="pg" style="justify-content:flex-end">
  <div style="position:absolute;inset:0;background:rgba(6,5,4,.62)"></div>
  <div style="position:relative;background:#14120F;border-top:1px solid rgba(242,237,230,.13);
              border-radius:12px 12px 0 0;padding:0 20px 24px;display:flex;flex-direction:column;max-height:88%">
    <div style="display:flex;align-items:center;justify-content:space-between;padding:20px 0 16px;
                border-bottom:1px solid rgba(242,237,230,.07)">
      <h2 style="font-size:16px;font-weight:600">设置</h2>
      <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="rgba(242,237,230,.42)" stroke-width="1.9" stroke-linecap="round" transform="rotate(45)">
        <path d="M12 5.4v13.2M5.4 12h13.2"/>
      </svg>
    </div>

    {group("时长")}
    {row("专注", "一个番茄的长度", "25", "分")}
    {row("短休息", "每个番茄之后", "5", "分")}
    {row("长休息", "完成一组之后", "15", "分")}
    {row("每组番茄", "几个番茄后进入长休息", "4", "个")}

    {group("自动化")}
    {srow("自动进入休息", "专注结束后不用手动点", True)}
    {srow("自动开始下一轮", "休息结束后直接进入专注", False)}

    {group("提醒")}
    {srow("提示音", "结束时响三声", True)}
    {srow("震动", "结束时震动提醒", True)}

    <div style="padding-top:16px">
      <div style="display:grid;place-items:center;height:46px;background:#E2552F;color:#170904;
                  font-size:14.5px;font-weight:600;border-radius:6px">完成</div>
    </div>
  </div>
</div>
"""


def main():
    src = io.open(PATH, encoding="utf-8").read()

    # 找到 initDemo 的整个函数体，整体替换
    start = src.index("  function initDemo() {")
    end = src.index("  initDemo();")
    head = src[:start]
    tail = src[end:]

    new_demo = '''  function initDemo() {

    /* ── 第一排：项目背景 ───────────────────────────── */
    addSection(40, "01 项目背景");

    const r1Title = addTitle(100, 90, "番茄钟", { fontSize: 60, fontWeight: 700 });
    const r1Desc = addText(100, below(r1Title, 14),
      "一台把注意力当仪表读数的番茄钟。\\n专注前写清这一轮做什么，休息时看到成果，结束后沉淀成记录。", { fontSize: 15, maxWidth: 460 });

    const tagsY = below(r1Desc, 18);
    const tag1 = addTag(100, tagsY, "仪表式表盘");
    const tag2 = addTag(rightOf(tag1, 8), tagsY, "任务绑定番茄");
    const tag3 = addTag(rightOf(tag2, 8), tagsY, "记录与习惯");
    addTag(rightOf(tag3, 8), tagsY, "Android 可安装");

    const cardsY = below(tag1, 26);
    const card1 = addContextCard(100, cardsY, 300, null, "给谁用",
      "<p>需要长时间专注、又不想被复杂工具打断的人。手机上单手操作，一眼读完当前状态。</p>" +
      "<ul><li>学生、写作者、开发者</li><li>想跟踪自己专注量的人</li></ul>");
    const card2 = addContextCard(420, cardsY, 300, null, "解决什么",
      "<ul><li>只有倒计时，不知道这一轮在做什么</li><li>番茄结束后没有沉淀，无法回顾</li><li>计时器好看但不可信（切后台就走偏）</li></ul>");
    const card3 = addContextCard(740, cardsY, 300, null, "三条主流程",
      "<ol style='list-style:none;padding:0'>" +
      "<li>① 选任务 → ④ 专注 → 休息</li>" +
      "<li>② 新建任务 → 估算番茄数</li>" +
      "<li>③ 查看记录 → 调整节奏</li></ol>");

    const notesY = maxY([card1, card2, card3], 30);
    const note1 = addNote(100, notesY, "设计要求",
      "表盘由 60 道真实刻度构成，进度沿刻度推进。刻度是仪表的一部分，不是装饰。");
    const note2 = addNote(rightOf(note1, 22), notesY, "取舍",
      "只保留三种模式与一条当前任务。任务与记录各占一屏，不塞进计时页。");

    /* ── 第二排：设计系统 ───────────────────────────── */
    const r2Start = maxY([card1, card2, card3, note1, note2], 90);
    addSection(r2Start, "02 设计系统");

    const dsY = r2Start + 60;
    const colorCard = addDesignSystemCard(100, dsY, 470, null, "color", {
      title: "色板 · 暖中性底 + 单强调色",
      html: `<div class="color-swatch-group" style="flex-wrap:wrap;gap:16px;">
        <div class="swatch-item"><div class="swatch-circle" style="background:#0D0C0A;border:1px solid rgba(255,255,255,.12)"></div><div class="swatch-name">底 ink-0</div><div class="swatch-hex">#0D0C0A</div></div>
        <div class="swatch-item"><div class="swatch-circle" style="background:#14120F"></div><div class="swatch-name">面 ink-1</div><div class="swatch-hex">#14120F</div></div>
        <div class="swatch-item"><div class="swatch-circle" style="background:#221F1A"></div><div class="swatch-name">抬 ink-3</div><div class="swatch-hex">#221F1A</div></div>
        <div class="swatch-item"><div class="swatch-circle" style="background:#F2EDE6"></div><div class="swatch-name">主文</div><div class="swatch-hex">#F2EDE6</div></div>
        <div class="swatch-item"><div class="swatch-circle" style="background:#A79C8F"></div><div class="swatch-name">次文</div><div class="swatch-hex">#A79C8F</div></div>
        <div class="swatch-item"><div class="swatch-circle" style="background:#E2552F"></div><div class="swatch-name">专注</div><div class="swatch-hex">#E2552F</div></div>
        <div class="swatch-item"><div class="swatch-circle" style="background:#6FA88A"></div><div class="swatch-name">短休息</div><div class="swatch-hex">#6FA88A</div></div>
        <div class="swatch-item"><div class="swatch-circle" style="background:#6E86A8"></div><div class="swatch-name">长休息</div><div class="swatch-hex">#6E86A8</div></div>
      </div>`
    });

    const typeCard = addDesignSystemCard(600, dsY, 420, null, "typography", {
      title: "字体 · 数字用等宽仪表字形",
      html: `<div class="type-sample-group">
        <div class="type-sample-row"><span class="type-sample-meta">读数<br>68px/300</span><span class="type-sample-text" style="font-family:Bahnschrift,monospace;font-size:40px;font-weight:300;letter-spacing:-.02em;font-variant-numeric:tabular-nums">25:00</span></div>
        <div class="type-sample-row"><span class="type-sample-meta">标题<br>24px/600</span><span class="type-sample-text" style="font-size:24px;font-weight:600">任务与记录</span></div>
        <div class="type-sample-row"><span class="type-sample-meta">正文<br>14.5px/400</span><span class="type-sample-text" style="font-size:14.5px">专注前写清这一轮做什么</span></div>
        <div class="type-sample-row"><span class="type-sample-meta">标签<br>10.5px/600</span><span class="type-sample-text" style="font-size:10.5px;font-weight:600;letter-spacing:.16em">本轮专注</span></div>
      </div>`
    });

    const compCard = addDesignSystemCard(1040, dsY, 300, null, "components", {
      title: "组件与刻度语言",
      html: `<div style="display:flex;flex-direction:column;gap:14px;">
        <button style="padding:11px 20px;border:none;border-radius:6px;background:#E2552F;color:#170904;font-size:13.5px;font-weight:600;cursor:pointer;">开始专注</button>
        <button style="padding:11px 20px;border-radius:6px;border:1px solid rgba(255,255,255,.13);background:transparent;color:#F2EDE6;font-size:13.5px;cursor:pointer;">跳过本轮</button>
        <div style="display:flex;gap:5px;align-items:center">
          <span style="width:22px;height:3px;background:#E2552F"></span>
          <span style="width:22px;height:3px;background:rgba(255,255,255,.13)"></span>
          <span style="width:22px;height:3px;background:rgba(255,255,255,.13)"></span>
          <span style="width:22px;height:3px;background:rgba(255,255,255,.13)"></span>
          <span style="margin-left:8px;font-size:11px;color:#A79C8F">组内进度</span>
        </div>
        <div style="display:flex;gap:3px;align-items:flex-end;height:22px">
          ${"<i style='width:2px;height:9px;background:rgba(255,255,255,.22);display:block'></i>".repeat(3)}
          ${"<i style='width:2px;height:9px;background:#E2552F;display:block'></i>".repeat(2)}
          <span style="margin-left:8px;font-size:11px;color:#A79C8F">任务番茄数</span>
        </div>
      </div>`
    });

    /* ── 第三排：设计稿 ─────────────────────────────── */
    const r3Start = maxY([colorCard, typeCard, compCard], 90);
    addSection(r3Start, "03 设计稿");

    const pagesY = r3Start + 60;
    const w = 390, h = 780, gap = 60;
    const p1 = addPage(100, pagesY, w, h, "计时 · 专注中", PAGE_TIMER);
    const p2 = addPage(100 + (w + gap), pagesY, w, h, "任务 · 清单", PAGE_TASKS);
    const p3 = addPage(100 + (w + gap) * 2, pagesY, w, h, "记录 · 统计", PAGE_STATS);
    const p4 = addPage(100 + (w + gap) * 3, pagesY, w, h, "设置 · 抽屉", PAGE_SETTINGS);
  }

'''

    src = head + new_demo + tail

    # 注入页面 HTML 常量
    inject = "  const PAGE_TIMER = " + repr(page_timer()) + ";\n"
    inject += "  const PAGE_TASKS = " + repr(page_tasks()) + ";\n"
    inject += "  const PAGE_STATS = " + repr(page_stats()) + ";\n"
    inject += "  const PAGE_SETTINGS = " + repr(page_settings()) + ";\n\n"
    src = src.replace("  function initDemo() {", inject + "  function initDemo() {", 1)

    io.open(PATH, "w", encoding="utf-8", newline="\n").write(src)
    print("canvas filled")


if __name__ == "__main__":
    main()
