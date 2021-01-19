FROM puckel/docker-airflow:latest
COPY ./requirements.txt /usr/local/.requirements.txt
RUN pip install --user psycopg2-binary
# RUN pip install -r /usr/local/.requirements.txt
ENV AIRFLOW_HOME=/usr/local/airflow
COPY ./airflow.cfg /usr/local/airflow/airflow.cfg
ENV PATH="/usr/local/airflow:${PATH}"
