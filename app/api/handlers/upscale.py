from PIL import Image, ImageEnhance
import cv2
import numpy as np
import aiohttp
from io import BytesIO
from environs import Env

env = Env()
env.read_env()


async def upscale(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.deepai.org/api/waifu2x",
            data={"image": url},
            headers={"api-key": env("DEEPAI_API_KEY")},
        ) as r:
            print("r is done", r)

            json = await r.json()
            print("json", json)
            url = json["output_url"]

            # or use a session you already have
            async with session.get(url) as resp:
                buffer = await resp.read()

            # get the byte array for opencv to read it
            file_bytes = np.frombuffer(bytearray(buffer), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            b, g, r = cv2.split(img)  # get b,g,r
            rgb_img = cv2.merge([r, g, b])  # switch it to rgb

            # # denoise
            dst = cv2.fastNlMeansDenoisingColored(rgb_img, None, 0.5, 0.5, 7, 21)

            # convert to PIL
            im = Image.fromarray(dst)

            # sharpen
            factor = 1.50
            enhancer = ImageEnhance.Sharpness(im)
            im_sharp = enhancer.enhance(factor)

            # contrast
            factor = 1.0375
            enhancer = ImageEnhance.Contrast(im_sharp)
            im_contrast = enhancer.enhance(factor)

            # save to buffer
            img_byte_arr = BytesIO()

            im_contrast.save(img_byte_arr, format="png", quality=100, subsampling=0)

            return img_byte_arr.getvalue()
