from PIL import Image, ImageEnhance
import cv2
import numpy as np
from io import BytesIO
from environs import Env
import magic
import requests

env = Env()
env.read_env()


def enhance(buffer):
    # get the byte array for opencv to read it
    file_bytes = np.frombuffer(bytearray(buffer), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(img)
    rgb_img = cv2.merge([r, g, b])  # switch it to rgb

    # denoise
    dst = cv2.fastNlMeansDenoisingColored(rgb_img, None, 0.5, 0.5, 7, 21)

    # convert to PIL
    im = Image.fromarray(dst)

    # sharpen
    factor = 1.50
    enhancer = ImageEnhance.Sharpness(im)
    im_sharp = enhancer.enhance(factor)

    # contrast
    factor = 1.03
    enhancer = ImageEnhance.Contrast(im_sharp)
    im_contrast = enhancer.enhance(factor)

    # save to buffer
    img_byte_arr = BytesIO()

    im_contrast.save(img_byte_arr, format="png", quality=100, subsampling=0)

    return img_byte_arr.getvalue()


def upscale(url: str):
    response = requests.get(url)
    buffer = response.content
    file_type = magic.from_buffer(buffer, mime=True)
    if "gif" in file_type:
        return buffer

    # big images don't need waifu2x
    file_bytes = np.frombuffer(bytearray(buffer), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    if w > 400 and h > 600:
        return enhance(buffer)

    # upscale then enhance
    response = requests.post(
        "https://api.deepai.org/api/waifu2x",
        data={"image": url},
        headers={"api-key": env("DEEP_AI_API_KEY")}
    )

    json = response.json()
    output_url = json["output_url"]
    
    response = requests.get(output_url)
    buffer = response.content
    
    return enhance(buffer)
