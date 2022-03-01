FROM alpine:3.14

WORKDIR /app

COPY . /app

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

CMD uvicorn server-main:app --host 0.0.0.0 --port 80
