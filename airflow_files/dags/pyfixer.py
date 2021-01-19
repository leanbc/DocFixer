from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago
import sys
import os
#adding to path directory above
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from python_callables.main import main,execute_ddl

args = {
    'owner': 'airflow',
    'start_date': days_ago(0)}


dag = DAG(
    dag_id='pyfixer_dag',
    default_args=args,
    schedule_interval='*/5 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
    template_searchpath='/usr/local/airflow/sql',
    tags=['example']
)

import_fx_data= PythonOperator(
    dag=dag,
    task_id='import_fx_data',
    provide_context=False,
    python_callable=main)


execute_ddl= PythonOperator(
    dag=dag,
    task_id='execute_ddl',
    provide_context=False,
    python_callable=execute_ddl)

execute_ddl >> import_fx_data


if __name__ == "__main__":
    dag.cli()