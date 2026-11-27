"""Generate 1200x630 share-card images for X/Twitter previews.

Runs before `jekyll build` (see .github/workflows/pages.yml). Writes:
  cards/site.png              - default card for the homepage and other pages
  cards/<entry-file-name>.png - one card per entry that has no cover image
The cards/ folder is generated on every build and is not committed.
"""
import pathlib
import re
import sys

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "cards"
FONTS = ROOT / "_cards" / "fonts"

W, H = 1200, 630
PAD = 72
BG = "#F6F8F5"
CARD = "#FFFFFF"
INK = "#15201A"
MUTED = "#59665E"
LINE = "#DCE2DA"
TYPE = {
    "thread": ("TH", "THREAD", "#1F4C8F"),
    "chart": ("CH", "CHART", "#A35C0E"),
    "historical": ("HX", "HISTORICAL", "#4E6A1E"),
}


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"  skipped {path.name}: bad front matter ({e})", file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


def wrap(draw, text, fnt, width, max_lines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textlength(last + "…", font=fnt) > width:
            last = last[:-1].rstrip()
        lines[-1] = last + "…"
    return lines


def fit_title(draw, title, width, max_height):
    for size in (104, 96, 88, 80, 72, 64, 58, 52):
        fnt = font("BarlowCondensed-Bold.woff", size)
        lh = int(size * 0.98)
        max_lines = max(1, max_height // lh)
        lines = wrap(draw, title, fnt, width, max_lines)
        if not lines[-1].endswith("…") or size == 52:
            return fnt, lines, lh
    return fnt, lines, lh


def render(path, eyebrow, title, accent, site):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # paper sheet with a type-coloured top bar, like the site's cards
    d.rectangle([40, 40, W - 40, H - 40], fill=CARD, outline=LINE, width=2)
    d.rectangle([40, 40, W - 40, 52], fill=accent)

    mono = font("IBMPlexMono-Medium.woff", 26)
    d.text((PAD + 8, 92), eyebrow, font=mono, fill=accent)

    title = title.upper()
    fnt, lines, lh = fit_title(d, title, W - 2 * PAD - 16, 330)
    y = 150
    for line in lines:
        d.text((PAD + 6, y), line, font=fnt, fill=INK)
        y += lh

    d.line([PAD + 8, H - 128, W - PAD - 8, H - 128], fill=LINE, width=2)
    foot = font("IBMPlexMono-Medium.woff", 24)
    handle = f"@{site['x_handle']}" if site.get("x_handle") else ""
    d.text((PAD + 8, H - 108), site.get("title", "").upper(), font=foot, fill=MUTED)
    if handle:
        tw = d.textlength(handle, font=foot)
        d.text((W - PAD - 8 - tw, H - 108), handle, font=foot, fill=INK)
    img.save(path, optimize=True)


def main():
    site = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8")) or {}
    OUT.mkdir(exist_ok=True)

    render(OUT / "site.png", "DEFENSE ANALYSIS ARCHIVE",
           site.get("title", "Archive"), "#1F4C8F", site)

    entries = sorted((ROOT / "_entries").glob("*.md"))
    # numbering matches _includes/catno.html: by date order within each type
    by_type = {}
    for p in entries:
        fm = front_matter(p)
        t = fm.get("type", "thread")
        if t not in TYPE:
            t = "thread"
        by_type.setdefault(t, []).append((str(fm.get("date", p.name[:10])), p, fm))

    made = 0
    for t, items in by_type.items():
        code, label, accent = TYPE[t]
        for i, (_, p, fm) in enumerate(sorted(items, key=lambda x: x[0]), start=1):
            if fm.get("image"):
                continue  # entries with their own cover image use that instead
            num = fm.get("number") or i
            eyebrow = f"{code}-{int(num):04d} · {label}"
            if t == "historical" and (fm.get("era") or fm.get("year")):
                eyebrow += f" · {fm.get('era') or fm.get('year')}"
            render(OUT / f"{p.stem}.png", eyebrow.upper(),
                   str(fm.get("title") or "Untitled"), accent, site)
            made += 1
    print(f"Share cards: site card + {made} entry card(s) written to cards/")


if __name__ == "__main__":
    main()
