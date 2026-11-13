"""Generate the pomodoro app icons.

Design: dark canvas with a soft warm glow, a thin progress ring, and a clean
tomato with a five-leaf crown.  Everything is drawn at 4x and downsampled so
small sizes stay crisp.

Compositing rule followed throughout: every layer is composited with
alpha_composite() over an opaque base, never pasted with a mask (which would
replace alpha and punch holes in the icon).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
os.makedirs(OUT, exist_ok=True)

BG = (13, 12, 11)
GLOW = (255, 107, 74)
TOMATO_DARK = (200, 62, 38)
TOMATO = (243, 94, 64)
TOMATO_LIGHT = (255, 146, 112)
LEAF_DARK = (26, 150, 104)
LEAF = (68, 210, 148)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)


def leaf_polygon(cx, cy, angle_deg, length, width, bend=0.16):
    """Closed tapered-leaf polygon with the base at (cx, cy) pointing at angle."""
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux

    def edge(sign):
        out = []
        steps = 12
        for i in range(steps + 1):
            t = i / steps
            w = width * math.sin(math.pi * (t ** 0.72)) * (1 - 0.30 * t)
            bx = cx + ux * length * t + px * bend * length * t * t
            by = cy + uy * length * t + py * bend * length * t * t
            out.append((bx + px * w * sign, by + py * w * sign))
        return out

    return edge(1.0) + edge(-1.0)[::-1]


def radial_glow(size, color, radius, alpha, center):
    n = size
    layer = Image.new("RGBA", (n, n), TRANSPARENT)
    d = ImageDraw.Draw(layer)
    steps = 90
    cx, cy = center
    for i in range(steps, 0, -1):
        t = i / steps
        r = radius * t
        a = int(alpha * (1 - t) ** 2.1)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    # drawing replaces pixels, so blend once against a clean transparent base
    return layer.filter(ImageFilter.GaussianBlur(n * 0.02))


def shadow(size, box, blur, alpha):
    n = size
    layer = Image.new("RGBA", (n, n), TRANSPARENT)
    ImageDraw.Draw(layer).ellipse(box, fill=(0, 0, 0, alpha))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def draw_icon(size, ring=True, glow=True):
    ss = 4
    n = size * ss
    S = float(n)

    # opaque base, then glow on top
    img = Image.new("RGBA", (n, n), BG + (255,))
    if glow:
        img = Image.alpha_composite(img, radial_glow(n, GLOW, S * 0.62, 46, (S * 0.5, S * 0.16)))

    cx = cy = S / 2
    body_r = S * 0.238
    by = cy + S * 0.030
    body = [cx - body_r, by - body_r * 0.97, cx + body_r, by + body_r * 0.97]

    # --- progress ring ---
    if ring:
        rr = S * 0.400
        stroke = int(S * 0.030)
        d = ImageDraw.Draw(img)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=WHITE + (22,), width=stroke)
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=-90, end=200,
              fill=TOMATO + (255,), width=stroke)

    # --- contact shadow under the tomato ---
    img = Image.alpha_composite(img, shadow(
        n, [cx - body_r * 0.95, by + body_r * 0.46, cx + body_r * 0.95, by + body_r * 1.12],
        S * 0.028, 130))

    # --- tomato body ---
    body_mask = Image.new("L", (n, n), 0)
    ImageDraw.Draw(body_mask).ellipse(body, fill=255)

    layer = Image.new("RGBA", (n, n), TRANSPARENT)
    ImageDraw.Draw(layer).ellipse(body, fill=TOMATO + (255,))
    img = Image.alpha_composite(img, layer)

    # bottom shading
    shade = Image.new("RGBA", (n, n), TRANSPARENT)
    ImageDraw.Draw(shade).ellipse(
        [cx - body_r * 1.25, by + body_r * 0.02, cx + body_r * 1.25, by + body_r * 1.45],
        fill=TOMATO_DARK + (200,))
    shade = shade.filter(ImageFilter.GaussianBlur(S * 0.055))
    img = Image.alpha_composite(img, Image.composite(shade, Image.new("RGBA", (n, n), TRANSPARENT), body_mask))

    # rim light, upper-left
    rim = Image.new("RGBA", (n, n), TRANSPARENT)
    ImageDraw.Draw(rim).arc(
        [cx - body_r * 0.985, by - body_r * 0.955, cx + body_r * 0.985, by + body_r * 0.955],
        start=158, end=292, fill=TOMATO_LIGHT + (190,), width=int(S * 0.013))
    rim = rim.filter(ImageFilter.GaussianBlur(S * 0.007))
    img = Image.alpha_composite(img, Image.composite(rim, Image.new("RGBA", (n, n), TRANSPARENT), body_mask))

    # specular highlight
    spec = Image.new("RGBA", (n, n), TRANSPARENT)
    ImageDraw.Draw(spec).ellipse(
        [cx - body_r * 0.62, by - body_r * 0.74, cx - body_r * 0.08, by - body_r * 0.26],
        fill=WHITE + (128,))
    spec = spec.filter(ImageFilter.GaussianBlur(S * 0.021))
    img = Image.alpha_composite(img, Image.composite(spec, Image.new("RGBA", (n, n), TRANSPARENT), body_mask))

    # --- leaf crown ---
    stem_y = by - body_r * 0.62
    leaf_len = body_r * 0.56
    leaf_w = body_r * 0.185
    angles = (-172, -134, -92, -50, -8, 32)

    leaves = Image.new("RGBA", (n, n), TRANSPARENT)
    ld = ImageDraw.Draw(leaves)
    for ang in angles:
        # the two side-most leaves are shortest, the front ones the longest
        k = 0.78 + 0.22 * math.cos(math.radians(ang + 92))
        ld.polygon(leaf_polygon(cx, stem_y, ang, leaf_len * k, leaf_w, bend=0.10),
                   fill=LEAF + (255,))
    # stem on top of the leaf bases
    ld.ellipse([cx - leaf_w * 0.38, stem_y - leaf_w * 0.46,
                cx + leaf_w * 0.38, stem_y + leaf_w * 0.30],
               fill=LEAF_DARK + (255,))
    leaf_mask = leaves.split()[3].filter(ImageFilter.GaussianBlur(S * 0.0015))
    img = Image.alpha_composite(img, Image.composite(leaves, Image.new("RGBA", (n, n), TRANSPARENT),
                                                     leaf_mask))

    # underside shading for the leaves
    lsh = Image.new("RGBA", (n, n), TRANSPARENT)
    lsd = ImageDraw.Draw(lsh)
    for ang in angles:
        k = 0.78 + 0.22 * math.cos(math.radians(ang + 92))
        lsd.polygon(leaf_polygon(cx, stem_y + leaf_w * 0.42, ang, leaf_len * k * 0.8,
                                 leaf_w * 0.55, bend=0.10),
                    fill=LEAF_DARK + (150,))
    lsh = lsh.filter(ImageFilter.GaussianBlur(S * 0.005))
    img = Image.alpha_composite(img, Image.composite(lsh, Image.new("RGBA", (n, n), TRANSPARENT), leaf_mask))

    return img.resize((size, size), Image.LANCZOS)


def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p, "PNG", optimize=True)
    print(f"{name:26s} {img.size[0]:>5}x{img.size[1]:<5} {os.path.getsize(p) // 1024:>4} KB")


if __name__ == "__main__":
    save(draw_icon(512), "icon-512.png")
    save(draw_icon(192), "icon-192.png")

    # maskable: art inside the 80% safe zone, full-bleed background
    maskable = Image.new("RGBA", (512, 512), BG + (255,))
    maskable = Image.alpha_composite(maskable, radial_glow(512, GLOW, 300, 40, (256, 100)))
    inner = draw_icon(512, ring=False).resize((350, 350), Image.LANCZOS)
    maskable.alpha_composite(inner, (81, 81))
    save(maskable, "icon-maskable-512.png")

    save(draw_icon(180, ring=False), "apple-touch-icon.png")
    save(draw_icon(64, ring=False), "favicon-64.png")
    save(draw_icon(1200), "og.png")
