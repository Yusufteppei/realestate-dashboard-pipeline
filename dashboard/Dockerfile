FROM python:3.9-alpine3.15

WORKDIR /dashboard

RUN pip install dash pandas plotly dash_core_components sqlalchemy psycopg2-binary 

RUN pip install dash_bootstrap_components

COPY . .

EXPOSE 8050:8050

CMD python main.py --container-name=dashboard-dash