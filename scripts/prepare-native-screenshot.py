from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
source = Path('C:/Users/16704/AppData/Local/Temp/codex-clipboard-f79587e6-cd0a-49e9-ba76-d835d6e056a5.png')
with Image.open(source) as image:
    image = image.convert('RGB')
    # Keep browser chrome and native layout; cover identifying items with
    # matching solid colors, and copy each gradient row behind the page avatar.
    draw = ImageDraw.Draw(image)
    cream = image.getpixel((1800, 190))
    green = image.getpixel((1900, 35))
    draw.rectangle((0, 158, image.width-1, 225), fill=cream)
    draw.rectangle((1915, 83, 2485, 153), fill=cream)
    draw.rectangle((2040, 0, 2300, 73), fill=green)
    for y in range(245, 336):
        draw.line((2440, y, 2540, y), fill=image.getpixel((2200, y)))
    # Remove only shortcut captions, retaining the three native icons.
    draw.rectangle((990, 984, 1590, 1036), fill=image.getpixel((900, 1000)))
    clean = image
    clean.thumbnail((1280, 800), Image.Resampling.LANCZOS)
    output = Image.new('RGB', (1280, 800), '#244C3D')
    output.paste(clean, ((1280-clean.width)//2, (800-clean.height)//2))
    output.save(root/'store-assets/screenshots/en/screenshot-1-browser.png')
    assert output.size == (1280,800)
