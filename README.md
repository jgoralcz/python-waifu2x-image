# Upscale images API
Upscale the images using openCV translation of waifu2x. It uses a denoise level of 1 and outputs as png. It then sharpens, contrasts, colors, and slightly brightens the image. It takes about 5 seconds to upscale and enhance an image from 225 x 350 to 450 x 700 using your CPU.

## Docker (Basically only way to run this without building everything)
`docker build -t python-image . && docker rm -f python-image || true && docker run --cpus 2 -m 2048m -d -p 8443:8443 --name python-image python-image`

## Docs
`url/doc` or `url/redoc`
