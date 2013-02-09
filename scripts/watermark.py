from PIL import Image, ImageDraw, ImageFont
from math import atan, degrees
import sys
import os

FONT = "/usr/share/fonts/truetype/droid/DroidSans.ttf"

def add_watermark(filename, text, outfilename):
    img = Image.open(filename).convert("RGB")
    watermark = Image.new("RGBA", (img.size[0], img.size[1]))
    draw = ImageDraw.ImageDraw(watermark, "RGBA")
    size = 0
    while True:
        size += 1
        nextfont = ImageFont.truetype(FONT, size)
        nexttextwidth, nexttextheight = nextfont.getsize(text)
        if nexttextwidth+nexttextheight/3 > watermark.size[0]:
            break
        font = nextfont
        textwidth, textheight = nexttextwidth, nexttextheight
    draw.setfont(font)
    draw.text(((watermark.size[0]-textwidth)/2,
               (watermark.size[1]-textheight)/2), text)
    watermark = watermark.rotate(degrees(atan(float(img.size[1])/
                                              img.size[0])),
                                 Image.BICUBIC)
    mask = watermark.convert("L").point(lambda x: min(x, 55))
    watermark.putalpha(mask)
    img.paste(watermark, None, watermark)
    img.save(outfilename)

if __name__ == "__main__":
    add_watermark('/tmp/hyde_site/content/media/photos/NYC/Tesla/tesla_model_x_high.jpg', '\xa9 Justin Judd', '/tmp/hyde_site/content/media/photos/NYC/Tesla/tesla_model_x_test.jpg' )
