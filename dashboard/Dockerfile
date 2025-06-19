FROM python:3.9-alpine3.15

WORKDIR /dashboard

RUN apk update && apk add git vim

RUN git clone https://github.com/Yusufteppei/realestate-dashboard-pipeline.git

RUN cd realestate-dashboard-pipeline/dashboard

RUN pip install dash pandas plotly dash_core_components sqlalchemy psycopg2-binary dash_bootstrap_components dash_design_kit

EXPOSE 8050:8050

CMD python main.py --container-name=dashboard-dash