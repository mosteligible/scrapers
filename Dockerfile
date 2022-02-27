FROM python:3

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

CMD uvicorn server-main:app --host 0.0.0.0 --port 80
