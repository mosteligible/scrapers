FROM python:3

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

CMD python3 main.py --url https://www.kijiji.ca/b-apartments-condos/mississauga-peel-region/c37l1700276
