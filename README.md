# Upscale images API
Upscale the images using your API key from deepai using waifu2x. Then it uses opencv to denoise the image slightly, then sharpens and contrasts them slightly as well.


## Installation
`pip3 install -r requirements.txt`

## Running locally
Set DEEP_AI_API_KEY, USERNAME, and PASSWORD as environment variables. \
`uvicorn app.main:app --reload --host 0.0.0.0 --port 8443`

## Debugging (for me)
`ip -4 addr show eth0` -- bug with wsl2 not working with localhost

## Docker
`docker build -t python-image . && docker rm -f python-image || true && docker run --cpus 4 -m 4096m -d -p 8443:8443 --name python-image python-image`

## Docs
`url/doc` or `url/redoc`
