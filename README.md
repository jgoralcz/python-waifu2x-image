# Upscale images API
Upscale the images using your API key from deepai using waifu2x. Then it uses opencv to denoise the image slightly, then sharpens and contrasts them slightly as well.

## ENV variables
DEEP_AI_API_KEY


## Installation
`pip3 install -r requirements.txt`


## Running locally
`uvicorn app.main:app --reload`

## Docs
`url/doc` or `url/redoc`
