FROM python:3.8

WORKDIR /usr/python

RUN apt-get update && apt-get install -y python3-opencv

COPY requirements.txt /usr/python/

RUN pip3 install -r requirements.txt

COPY app /usr/python/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
