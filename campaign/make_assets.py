"""Builds the first batch of Instagram images for the Forge campaign.

Run:  python3 campaign/make_assets.py      (needs Pillow; macOS system fonts)
Out:  campaign/assets/

Dragon art is fetched from the app's public avatar CDN (not stored in git), so
the images stay in sync if the art is replaced (ROADMAP 3.5/3.6). Style follows
the brand doc: flat, cream/copper/sage/charcoal, no gradients or shadows.

Deliberately NOT used: copper/mature-balanced.png (opaque grey background and
a garbled text artifact in its bottom-right corner) and
copper/fledgling-gentle.png (a small mark on its right edge).
"""
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

CDN = "https://d3ecy6kiy1ze2c.cloudfront.net"
CREAM, CHARCOAL, COPPER, SAGE = "#f5f1e8", "#2c3e50", "#b87333", "#9caf88"
FONT = "/System/Library/Fonts/Avenir Next.ttc"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
CACHE = os.path.join(HERE, ".art-cache")
W, H = 1080, 1350  # Instagram portrait feed post


def font(style, size):
    index = {"bold": 0, "demi": 2, "medium": 5, "regular": 7, "heavy": 8}[style]
    return ImageFont.truetype(FONT, size, index=index)


def art(name):
    """Dragon PNG (e.g. 'copper/egg'), cached, trimmed to its visible area."""
    path = os.path.join(CACHE, name.replace("/", "_") + ".png")
    if not os.path.exists(path):
        os.makedirs(CACHE, exist_ok=True)
        urllib.request.urlretrieve(f"{CDN}/{name}.png", path)
    im = Image.open(path).convert("RGBA")
    return im.crop(im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox())


def paste_fit(canvas, im, box, anchor="center"):
    """Scales im to fit inside box=(x, y, w, h), centred."""
    x, y, w, h = (int(v) for v in box)
    scale = min(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    canvas.paste(im, (x + (w - im.width) // 2, y + (h - im.height) // 2), im)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def text_block(draw, text, fnt, fill, x, y, width, spacing=1.25, center=False):
    for line in wrap(draw, text, fnt, width):
        tx = x + (width - draw.textlength(line, font=fnt)) / 2 if center else x
        draw.text((tx, y), line, font=fnt, fill=fill)
        y += fnt.size * spacing
    return y


def footer(draw, w, h, label="FORGE"):
    f = font("demi", 26)
    draw.text(((w - draw.textlength(label, font=f)) / 2 - 0, h - 74), label, font=f, fill=COPPER)


def slide(name, dragon=None, eyebrow=None, title=None, body=None, big=None, cta=False, w=W, h=H):
    canvas = Image.new("RGB", (w, h), CREAM)
    d = ImageDraw.Draw(canvas)
    pad = 90
    y = 110
    if eyebrow:
        d.text((pad, y), eyebrow.upper(), font=font("demi", 28), fill=COPPER)
        y += 70
    if title:
        y = text_block(d, title, font("bold", 76), CHARCOAL, pad, y, w - 2 * pad)
    if dragon is not None:
        top = y + 20
        bottom = h - (330 if body else 470 if cta else 200)
        paste_fit(canvas, dragon, (pad, top, w - 2 * pad, bottom - top))
    if big:  # a large step numeral in the empty middle of a text slide
        f = font("heavy", 460)
        top, bottom = y + 20, h - 330
        l, t, r, b = d.textbbox((0, 0), big, font=f)
        d.text(((w - (r - l)) / 2 - l, top + (bottom - top - (b - t)) / 2 - t), big, font=f, fill=SAGE)
    if body:
        text_block(d, body, font("medium", 40), CHARCOAL, pad, h - 310, w - 2 * pad, center=True)
    if cta:
        bw, bh = 640, 110
        bx, by = (w - bw) // 2, h - 330
        d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=24, fill=SAGE)
        f = font("bold", 42)
        d.text((bx + (bw - d.textlength("Link in bio", font=f)) / 2, by + 30), "Link in bio", font=f, fill=CHARCOAL)
    footer(d, w, h)
    return canvas


def save(img, folder, name):
    os.makedirs(os.path.join(OUT, folder), exist_ok=True)
    img.save(os.path.join(OUT, folder, name), optimize=True)
    print("wrote", folder, name)


def linkedin_banner(scale=1):
    """LinkedIn profile banner, 1584x396 (scale=2 for a sharper 3168x792 upload).

    Layout rules, measured from a real desktop screenshot: the profile photo is a
    ~314 px circle at banner scale, spanning x 50-370 and from y~150 down, so all
    text starts at x=430. The mobile app crops the edges, so keep everything
    that matters inside x 430-1520, y 40-360. The four dragon stages grow left to right.
    """
    S = scale
    w, h = 1584 * S, 396 * S
    im = Image.new("RGB", (w, h), CREAM)
    d = ImageDraw.Draw(im)

    x = 430 * S
    d.text((x, 62 * S), "FORGE", font=font("demi", 22 * S), fill=COPPER)
    y = 108 * S
    for line in ("Build your dragon,", "build yourself."):
        d.text((x, y), line, font=font("bold", 46 * S), fill=CHARCOAL)
        y += 58 * S
    d.text((x, y + 14 * S), "Strength training with a companion", font=font("medium", 22 * S), fill=CHARCOAL)
    d.text((x, y + 44 * S), "that grows as you do.", font=font("medium", 22 * S), fill=CHARCOAL)
    d.text((x, 338 * S), "forge-app.ca", font=font("demi", 22 * S), fill=COPPER)

    stages = [("copper/egg", 76), ("copper/hatchling-balanced", 108),
              ("copper/fledgling-balanced", 160), ("copper/mature-fierce", 214)]
    gap = 14 * S
    sized = []
    for name, height in stages:
        dragon = art(name)
        scale_f = height * S / dragon.height
        sized.append(dragon.resize((round(dragon.width * scale_f), round(dragon.height * scale_f)), Image.LANCZOS))
    # Right-align the group to the margin (1520 of 1584) so nothing is clipped.
    cx = 1520 * S - (sum(dr.width for dr in sized) + gap * (len(sized) - 1))
    assert cx >= 880 * S, "stages overlap the text; shrink them"
    for dragon in sized:
        im.paste(dragon, (cx, 360 * S - dragon.height), dragon)
        cx += dragon.width + gap
    return im


def main():
    egg = art("copper/egg")
    hatch = art("copper/hatchling-balanced")
    fledge = art("copper/fledgling-balanced")
    mature = art("copper/mature-fierce")

    # 1. Carousel: the four stages (thresholds from src/shared/avatar.py).
    stages = [
        slide("hook", dragon=egg, eyebrow="Meet Forge", title="Every workout hatches something.",
              body="Swipe to watch a dragon grow"),
        slide("egg", dragon=egg, eyebrow="Stage 1 · Egg", title="It starts as an egg.",
              body="Log your first workout and it begins to stir."),
        slide("hatch", dragon=hatch, eyebrow="Stage 2 · Hatchling", title="Then it hatches.",
              body="After 20,000 lbs of lifting, total. Brave, curious, just beginning."),
        slide("fledge", dragon=fledge, eyebrow="Stage 3 · Fledgling", title="Then it finds its stride.",
              body="At 50,000 lbs. Stronger, steadier, building momentum."),
        slide("mature", dragon=mature, eyebrow="Stage 4 · Mature", title="Then it takes command.",
              body="At 100,000 lbs. The dragon you built, one workout at a time."),
        slide("cta", dragon=egg, eyebrow="Private beta · iPhone", title="Ready to hatch yours?", cta=True),
    ]
    for i, s in enumerate(stages, 1):
        save(s, "carousel-four-stages", f"slide-{i}.png")

    # 2. Carousel: gentle / balanced / fierce (intensity = days trained in the last 7).
    gentle, balanced, fierce = (art(f"copper/hatchling-{m}") for m in ("gentle", "balanced", "fierce"))
    moods = [
        slide("hook", dragon=balanced, eyebrow="How your dragon feels", title="Your dragon notices how you show up.",
              body="Swipe to see how"),
        slide("gentle", dragon=gentle, eyebrow="Gentle", title="A light week? It rests with you.",
              body="Fewer than 2 training days. No guilt, no lecture. It waits."),
        slide("balanced", dragon=balanced, eyebrow="Balanced", title="2–3 days? Steady and calm.",
              body="A rhythm you can keep. This is most of us, most weeks."),
        slide("fierce", dragon=fierce, eyebrow="Fierce", title="4 or more? It's on a roll.",
              body="Hot streak, big energy. And it relaxes again when you do."),
        slide("cta", dragon=balanced, eyebrow="Private beta · iPhone", title="Meet yours.", cta=True),
    ]
    for i, s in enumerate(moods, 1):
        save(s, "carousel-moods", f"slide-{i}.png")

    # 3. Single post: the promise.
    post = slide("promise", dragon=hatch, eyebrow="Our promise", title="No leaderboards. No shame.",
                 body="Just your progress, made visible.")
    save(post, "single", "no-leaderboards-no-shame.png")

    # 4. Story frame for the invite link sticker (1080x1920; sticker goes in the lower third).
    story = slide("story", dragon=egg, eyebrow="Private beta · iPhone", title="Request your invite.",
                  body="Tap the link below", w=1080, h=1920)
    save(story, "story", "request-invite.png")

    # 5. Profile picture: the egg on cream (Instagram crops to a circle, so keep it centred and small).
    avatar = Image.new("RGB", (1080, 1080), CREAM)
    paste_fit(avatar, egg, (270, 190, 540, 700))
    save(avatar, "profile", "profile-picture.png")

    # 8. LinkedIn banner (personal profile), 1x and 2x.
    save(linkedin_banner(1), "linkedin", "banner-1584x396.png")
    save(linkedin_banner(2), "linkedin", "banner-3168x792.png")

    # 6. Single: pick your dragon (2x2 of the four accent colours, hatchling stage).
    pick = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(pick)
    d.text((90, 110), "PICK YOURS", font=font("demi", 28), fill=COPPER)
    d.text((90, 180), "Which dragon is yours?", font=font("bold", 76), fill=CHARCOAL)
    cell, gap, top = 360, 60, 330
    for i, color in enumerate(("copper", "sage", "gold", "charcoal")):
        cx = (W - (2 * cell + gap)) // 2 + (i % 2) * (cell + gap)
        cy = top + (i // 2) * (cell + 50 + gap)
        paste_fit(pick, art(f"{color}/hatchling-balanced"), (cx, cy, cell, cell))
        label = color.capitalize()
        f = font("demi", 36)
        d.text((cx + (cell - d.textlength(label, font=f)) / 2, cy + cell + 8), label, font=f, fill=CHARCOAL)
    footer(d, W, H)
    save(pick, "single", "pick-your-dragon.png")

    # 7. Carousel: how to join the beta (matches the site: you request, then get a TestFlight invite).
    join = [
        slide("hook", dragon=egg, eyebrow="Private beta · iPhone", title="How to join the Forge beta.",
              body="Three steps. No payment."),
        slide("s1", big="1", eyebrow="Step 1", title="Request an invite.",
              body="Tap the link in our bio, pop in your email, and you're on the list."),
        slide("s2", big="2", eyebrow="Step 2", title="Get your TestFlight invite.",
              body="We email you a link. Open it on your iPhone to install Forge through Apple's TestFlight app."),
        slide("s3", dragon=hatch, eyebrow="Step 3", title="Hatch your egg.",
              body="Log a workout and your dragon starts to stir."),
        slide("expect", dragon=hatch, eyebrow="What to expect", title="It's still being built.",
              body="iPhone only for now. Some rough edges. Tell us what you think. It shapes what Forge becomes."),
        slide("cta", dragon=egg, eyebrow="Private beta · iPhone", title="Ready when you are.", cta=True),
    ]
    for i, sl in enumerate(join, 1):
        save(sl, "carousel-how-to-join", f"slide-{i}.png")


if __name__ == "__main__":
    main()
