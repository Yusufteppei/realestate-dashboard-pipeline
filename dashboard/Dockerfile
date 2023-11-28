FROM python:3.9-alpine3.15

WORKDIR /dashboard

RUN pip install -r reqs.txt

RUN apk update

RUN apk add git

RUN apk add vim

RUN git clone https://github.com/Yusufteppei/realestate-dashboard-pipeline.git

EXPOSE 8050:8050

CMD python realestate-dashboard-pipeline/dashboard/main.py --container-name=dashboard-dash