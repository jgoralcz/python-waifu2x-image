FROM joshgor01/waifu2x-ubuntu-deps:latest

COPY ./waifu2x /waifu2x
COPY ./nsfw_detector /nsfw_detector

RUN chmod +x /waifu2x/build.sh

RUN /waifu2x/build.sh

WORKDIR /usr/python

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt /usr/python/

RUN pip3 install -r requirements.txt

COPY app /usr/python/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8443"]
