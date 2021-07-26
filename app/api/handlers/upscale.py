from PIL import Image, ImageEnhance
import cv2
import numpy as np
import aiohttp
from io import BytesIO
from environs import Env
import magic

env = Env()
env.read_env()


def enhance(buffer):
    # get the byte array for opencv to read it
    file_bytes = np.frombuffer(bytearray(buffer), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(img)
    rgb_img = cv2.merge([r, g, b])  # switch it to rgb

    # denoise
    dst = cv2.fastNlMeansDenoisingColored(rgb_img, None, 0.8, 0.8, 7, 21)

    # convert to PIL
    im = Image.fromarray(dst)

    # sharpen
    factor = 1.55
    enhancer = ImageEnhance.Sharpness(im)
    im_sharp = enhancer.enhance(factor)

    # contrast
    factor = 1.05
    im_contrast = ImageEnhance.Contrast(im_sharp).enhance(factor)

    # brightness
    factor = 1.005
    im_brightness = ImageEnhance.Brightness(im_sharp).enhance(factor)

    # save to buffer
    img_byte_arr = BytesIO()

    im_brightness.save(img_byte_arr, format="png", quality=100, subsampling=0)

    return img_byte_arr.getvalue()


async def upscale(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            buffer = await resp.read()

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
            async with session.get(url) as resp:
                buffer = await resp.read()
                async with session.post(
                    "https://api.deepai.org/api/waifu2x",
                    data={"image": url},
                    headers={"api-key": env("DEEP_AI_API_KEY")},
                ) as r:

                    json = await r.json()
                    output_url = json["output_url"]

                    async with session.get(output_url) as resp:
                        buffer = await resp.read()

                        return enhance(buffer)
