"""First cut of Reel 1 ("One workout. One hatch.") from the raw simulator capture.

Run:  python3 campaign/edit_reel.py [raw.mp4] [out.mp4]
In:   campaign/footage/reel-hatch-raw.mp4  (scripts/record_reel.sh <udid> out.mp4 hatch)
Out:  campaign/footage/reel-hatch-cut.mp4  (1080x1920, 30 fps, ~25 s, silent)

Needs ffmpeg and Pillow. Segment times below are seconds in the RAW file and
were read off a recording; if you re-record, re-check them (the take varies by
a second or two). Brand style: flat cream/charcoal/copper, no gradients.
"""
import os
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "footage", "reel-hatch-raw.mp4")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "footage", "reel-hatch-cut.mp4")
CDN = "https://d3ecy6kiy1ze2c.cloudfront.net"
CREAM, CHARCOAL, COPPER, SAGE = "#f5f1e8", "#2c3e50", "#b87333", "#9caf88"
FONT = "/System/Library/Fonts/Avenir Next.ttc"
W, H = 1080, 1920
PHONE_H = 1480
PHONE_W = round(PHONE_H * 1206 / 2622)  # source is 1206x2622
PX, PY = (W - PHONE_W) // 2, 150

# (start, end, speed, caption) in seconds of the 30 fps conversion of the raw
# take (footage/reel-hatch-30fps.mp4 - scrub that file, not the raw one: simctl
# timestamps make seeks in the raw file land seconds off). Output length of a
# segment is (end - start) / speed.
SEGMENTS = [
    (13.5, 17.5, 1.6, "One workout."),          # Home, the egg
    (18.5, 24.5, 2.0, "Log a lift."),           # sheet opens, title typed
    (24.5, 31.0, 2.2, "Quick search."),         # exercise search + pick
    (31.5, 55.5, 4.8, "Tick off your sets."),   # sets entered and checked
    (55.5, 57.0, 3.0, None),                    # Finish tap
    (60.0, 65.5, 1.0, "Your dragon hatched."),  # celebration
    (70.0, 73.0, 1.2, "Every set counts."),     # Progress
]
END_CARD_SECONDS = 3.0


def font(size, index=0):  # index 0 = Avenir Next Bold
    return ImageFont.truetype(FONT, size, index=index)


def centered(draw, y, text, fnt, fill):
    draw.text(((W - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def phone_frame(path):
    """Cream everywhere except a rounded window where the phone video shows."""
    im = Image.new("RGBA", (W, H), CREAM)
    hole = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hole).rounded_rectangle((PX, PY, PX + PHONE_W, PY + PHONE_H), radius=64, fill=255)
    im.putalpha(Image.eval(hole, lambda v: 255 - v))
    ImageDraw.Draw(im).rounded_rectangle((PX - 3, PY - 3, PX + PHONE_W + 3, PY + PHONE_H + 3),
                                         radius=67, outline=CHARCOAL, width=6)
    # Keep the ring from being cut by the hole: redraw it on top where hole is.
    im.save(path)


def caption(path, text):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if text:
        f = font(54)
        tw = d.textlength(text, font=f)
        pw, ph = tw + 90, 120
        x, y = (W - pw) / 2, 1440  # inside the safe area (above the bottom ~340 px)
        d.rounded_rectangle((x, y, x + pw, y + ph), radius=60, fill=CREAM, outline=COPPER, width=4)
        d.text((x + 45, y + (ph - 54) / 2 - 8), text, font=f, fill=CHARCOAL)
    f = font(26, 5)
    centered(d, 1650, "Demo account", f, (44, 62, 80, 190))
    im.save(path)


def end_card(path):
    import urllib.request
    egg_path = os.path.join(HERE, ".art-cache", "copper_egg.png")
    if not os.path.exists(egg_path):
        os.makedirs(os.path.dirname(egg_path), exist_ok=True)
        urllib.request.urlretrieve(f"{CDN}/copper/egg.png", egg_path)
    egg = Image.open(egg_path).convert("RGBA")
    egg = egg.crop(egg.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox())
    im = Image.new("RGB", (W, H), CREAM)
    scale = 620 / egg.height
    egg = egg.resize((round(egg.width * scale), 620), Image.LANCZOS)
    im.paste(egg, ((W - egg.width) // 2, 330), egg)
    d = ImageDraw.Draw(im)
    centered(d, 1010, "Forge", font(110), CHARCOAL)
    centered(d, 1150, "PRIVATE BETA · IPHONE", font(34, 2), COPPER)
    f = font(48, 5)
    centered(d, 1260, "Request an invite", f, CHARCOAL)
    centered(d, 1325, "Link in bio", f, CHARCOAL)
    im.save(path)


def main():
    tmp = tempfile.mkdtemp()
    # simctl records only when the screen changes (variable frame rate), so a
    # static screen has no frames inside a trim window. Make it constant first.
    global RAW
    cfr = os.path.join(os.path.dirname(OUT), "reel-hatch-30fps.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", RAW, "-vf", "fps=30", "-an",
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", cfr], check=True)
    RAW = cfr
    frame = os.path.join(tmp, "frame.png")
    phone_frame(frame)
    caps = []
    for i, (_, _, _, text) in enumerate(SEGMENTS):
        p = os.path.join(tmp, f"cap{i}.png")
        caption(p, text)
        caps.append(p)
    card = os.path.join(tmp, "card.png")
    end_card(card)

    inputs = ["-i", RAW, "-i", frame]
    for p in caps:
        inputs += ["-i", p]
    inputs += ["-loop", "1", "-t", str(END_CARD_SECONDS), "-i", card]
    n = len(SEGMENTS)
    parts = [f"[0:v]split={n}" + "".join(f"[r{i}]" for i in range(n)),
             f"[1:v]split={n}" + "".join(f"[fr{i}]" for i in range(n))]
    labels = []
    for i, (a, b, speed, _) in enumerate(SEGMENTS):
        dur = (b - a) / speed
        parts.append(
            f"[r{i}]trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{speed},fps=30,scale={PHONE_W}:{PHONE_H}[p{i}];"
            f"color=c={CREAM}:s={W}x{H}:r=30:d={dur:.3f}[bg{i}];"
            f"[bg{i}][p{i}]overlay={PX}:{PY}[o{i}];"
            f"[o{i}][fr{i}]overlay=0:0[f{i}];"
            f"[f{i}][{2 + i}:v]overlay=0:0,format=yuv420p[s{i}]"
        )
        labels.append(f"[s{i}]")
    parts.append(f"[{2 + n}:v]fps=30,scale={W}:{H},format=yuv420p[end]")
    parts.append("".join(labels) + "[end]" + f"concat=n={n + 1}:v=1:a=0[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(parts),
           "-map", "[v]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", OUT]
    subprocess.run(cmd, check=True)
    total = sum((b - a) / s for a, b, s, _ in SEGMENTS) + END_CARD_SECONDS
    print(f"wrote {OUT} (~{total:.1f} s)")


if __name__ == "__main__":
    main()
