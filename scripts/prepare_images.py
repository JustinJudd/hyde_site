from PIL import Image, ImageDraw, ImageFont
import PIL
from math import atan, degrees
import sys
import os

FONT = "/usr/share/fonts/truetype/droid/DroidSans.ttf"
web_basewidth = 640
high_basewidth = 1920

def add_watermark_files(filename, text, outfilename):
    img = Image.open(filename).convert("RGB")
    watermarked = add_watermark(img, text) 
    watermarked.save(outfilename)
    
def add_watermark(img, text):
    img = img.convert("RGB")
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
    return img
    
    
def deinterlace_image_files(filename, outfilename):
    downsized = deinterlace_image(img=Image.open(filename))
    downsized.save(outputfilename)
    
def deinterlace_image(img):
    size=list(img.size)
    size[0] /= 2
    size[1] /= 2
    return img.resize(size, Image.NEAREST) # NEAREST drops the lines

if __name__ == "__main__":	
    #image_base = '/tmp/hyde_site/content/media/photos/NYC/Tesla/tesla_model_x'
    image_base = '/tmp/hyde_site/content/media/photos/NYC/statue_of_liberty'
    full_img_file = image_base + '_full.jpg'
    #high_img_file = image_base + '_high.jpg'
    high_img_file = image_base + '_high_test.jpg'
    #web_img_file = image_base + '_web.jpg'
    web_img_file = image_base + '_web_test.jpg'
    
    full_img=Image.open(full_img_file)
    
    wpercent = (high_basewidth / float(full_img.size[0]))
    hsize = int((float(full_img.size[1]) * float(wpercent)))
    high_img = full_img.resize((high_basewidth, hsize), PIL.Image.ANTIALIAS)
    high_img.save(high_img_file)
    
    wpercent = (web_basewidth / float(full_img.size[0]))
    hsize = int((float(full_img.size[1]) * float(wpercent)))
    web_img = full_img.resize((web_basewidth, hsize), PIL.Image.ANTIALIAS)
    web_img = add_watermark(web_img, '\xa9 Justin Judd' )
    web_img.save(web_img_file)
