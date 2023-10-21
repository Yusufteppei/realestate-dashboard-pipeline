FROM python:3.9-alpine3.15

WORKDIR /dashboard

RUN pip install dash pandas cdata plotly dash_core_components dash_html_components

RUN pip install sqlalchemy psycopg2-binary

COPY . .

EXPOSE 8050:8050

CMD python main.py