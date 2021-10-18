from PIL import Image
import imagehash
import requests
from io import BytesIO

def imagehashed(url: str):
    response = requests.get(url)
    buffer = response.content

    im = Image.open(BytesIO(buffer))
    avg_hash = imagehash.average_hash(im)

    return { "hash": str(avg_hash)}
