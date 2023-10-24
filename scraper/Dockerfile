FROM python:3.9-alpine3.15

WORKDIR /home/scraper

RUN pip install pandas requests bs4 lxml mysql-connector-python psycopg2-binary sqlalchemy

RUN apk update

RUN apk add git

RUN git clone https://github.com/Yusufteppei/realestate-dashboard-pipeline.git

#RUN python realestate-dashboard-pipeline/scraper/scrape.py;

CMD python realestate-dashboard-pipeline/scraper/scrape.py; python -m http.server 8000


# CHANGE WORKDIR TO NIG_PROPS