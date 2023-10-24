FROM python:3.9-alpine3.15

WORKDIR /dashboard

RUN pip install dash pandas plotly dash_core_components sqlalchemy psycopg2-binary dash_bootstrap_components

RUN git clone https://github.com/Yusufteppei/realestate-dashboard-pipeline.git

EXPOSE 8050:8050

CMD python realestate-dashboard-pipeline/dashboard/main.py --container-name=dashboard-dash