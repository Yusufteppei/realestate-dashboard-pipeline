FROM python:3.9-alpine3.15

WORKDIR /home/scraper

RUN pip install pandas requests bs4 lxml mysql-connector-python psycopg2-binary

RUN pip install sqlalchemy

COPY . .

CMD python main.py; python -m http.server 8000

