from PIL import Image, ImageEnhance
from io import BytesIO
from environs import Env
import magic
import requests
import subprocess
import uuid
import os

env = Env()
env.read_env()

def enhance(im):
    w, h = im.size
    if w < 400 and h < 600:
        # sharpen
        factor = 2.5
        im = ImageEnhance.Sharpness(im).enhance(factor)
    else:
        factor = 1.25
        im = ImageEnhance.Sharpness(im).enhance(factor)

    # contrast
    factor = 1.115
    im = ImageEnhance.Contrast(im).enhance(factor)
    
    # color
    factor = 1.015
    im = ImageEnhance.Color(im).enhance(factor)

    # brightness
    factor = 1.004
    im = ImageEnhance.Brightness(im).enhance(factor)

    # save to buffer
    img_byte_arr = BytesIO()
    im.save(img_byte_arr, format="png", quality=100, subsampling=0)

    return img_byte_arr.getvalue()

def upscale(url: str):
    response = requests.get(url)
    buffer = response.content
    file_type = magic.from_buffer(buffer, mime=True)
    if "gif" in file_type:
        return buffer

    # big images don't need waifu2x
    im = Image.open(BytesIO(buffer))
    w, h = im.size
    
    if w > 450 and h > 650:
        return buffer

    # prepare for waifu2x
    file_name = "/data/" + str(uuid.uuid1())
    inFile = file_name + ".png"
    outFile = file_name + "_out.png"
    im.save(inFile)
        
    # waifu2x it
    if w > 400 and h > 600:
        subprocess.run(["/waifu2x-cpp/waifu2x-converter-cpp", "--disable-gpu", "-m noise", "--noise-level 2", "-s", "-i", inFile, "-o", outFile])
    else:
        subprocess.run(["/waifu2x-cpp/waifu2x-converter-cpp", "--disable-gpu", "-m noise-scale", "--noise-level 2", "-s", "-i", inFile, "-o", outFile])

    im = Image.open(outFile)
    os.remove(outFile)
    
    img_byte_arr = BytesIO()
    im.save(img_byte_arr, format="png", quality=100, subsampling=0)

    return enhance(im)
