from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "social-preview.png"
ICON = ROOT / "eir-icon.png"

WIDTH = 1200
HEIGHT = 630


def rounded_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype("/System/Library/Fonts/SFNSRounded.ttf", size=size)


def system_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size=size)


def draw_gradient_background(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#FAFAF7")

    top_left = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    tl_draw = ImageDraw.Draw(top_left)
    tl_draw.ellipse((-120, -120, 380, 380), fill=(212, 167, 106, 56))
    top_left = top_left.filter(ImageFilter.GaussianBlur(36))
    base.alpha_composite(top_left)

    top_right = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    tr_draw = ImageDraw.Draw(top_right)
    tr_draw.ellipse((840, -110, 1270, 320), fill=(139, 184, 206, 60))
    top_right = top_right.filter(ImageFilter.GaussianBlur(42))
    base.alpha_composite(top_right)

    vignette = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    vg_draw = ImageDraw.Draw(vignette)
    vg_draw.rectangle((0, 0, WIDTH, HEIGHT), outline=(231, 229, 228, 255), width=2)
    base.alpha_composite(vignette)


def draw_breathing_orb(base: Image.Image) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = 895, 336

    draw.ellipse((cx - 128, cy - 128, cx + 128, cy + 128), outline=(161, 98, 7, 28), width=28)
    draw.ellipse((cx - 110, cy - 110, cx + 110, cy + 110), outline=(20, 184, 166, 58), width=2)
    draw.ellipse((cx - 84, cy - 84, cx + 84, cy + 84), fill=(255, 255, 255, 255))
    draw.ellipse((cx - 84, cy - 84, cx + 84, cy + 84), outline=(255, 249, 240, 255), width=18)

    layer = layer.filter(ImageFilter.GaussianBlur(0.5))
    base.alpha_composite(layer)

    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((cx - 100, cy - 100, cx + 100, cy + 100), fill=(255, 249, 240, 170))
    glow_draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=(20, 184, 166, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    base.alpha_composite(glow)

    center = ImageDraw.Draw(base)
    time_font = rounded_font(34)
    status_font = system_font(20)
    center.text((cx, cy - 18), "00:00", fill="#1C1917", font=time_font, anchor="mm")
    center.text((cx, cy + 22), "Breathe.", fill="#78716C", font=status_font, anchor="mm")


def draw_brand(draw: ImageDraw.ImageDraw, icon: Image.Image) -> None:
    pill_box = (84, 72, 310, 136)
    draw.rounded_rectangle(pill_box, radius=28, fill=(255, 255, 255), outline="#E7E5E4", width=2)

    icon_bg = Image.new("RGBA", (56, 56), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(icon_bg)
    bg_draw.rounded_rectangle((0, 0, 56, 56), radius=18, fill="#FFFFFF")
    icon_bg.alpha_composite(icon.resize((56, 56)))
    base_x, base_y = 96, 76
    preview.alpha_composite(icon_bg, (base_x, base_y))

    draw.text((168, 104), "Eir Space", fill="#1C1917", font=rounded_font(24), anchor="lm")


def draw_copy(draw: ImageDraw.ImageDraw) -> None:
    quote_font = rounded_font(76)
    body_font = system_font(26)
    footer_font = system_font(24)

    quote = "In doing nothing,\nnothing is missing."
    draw.multiline_text(
        (92, 208),
        quote,
        fill="#1C1917",
        font=quote_font,
        spacing=6,
        align="left",
    )

    body = "A quiet place on the internet where nothing is asked of you."
    draw.text((96, 430), body, fill="#78716C", font=body_font)

    draw.text((96, 560), "Nothing by Eir Space", fill="#78716C", font=footer_font)
    draw.text((1092, 560), "nothing.eir.space", fill="#A16207", font=footer_font, anchor="ra")


preview = Image.new("RGBA", (WIDTH, HEIGHT), "#FAFAF7")
draw_gradient_background(preview)
icon = Image.open(ICON).convert("RGBA")
draw_breathing_orb(preview)
draw = ImageDraw.Draw(preview)
draw_brand(draw, icon)
draw_copy(draw)
preview.convert("RGB").save(OUT, "PNG", optimize=True)
