import os
import sys
if os.path.basename(os.getcwd()) == 'python_callables':
    os.chdir(os.path.dirname(os.getcwd()))
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from helpers.sql.execute_sql_files import connect
from helpers.fixer.Fixer_data import Fixer_data
from helpers.sql.execute_sql_files import connect,execute_file

def execute_ddl():
    
    cur=connect(
        host='postgres',
        database='airflow',
        user='airflow',
        password='airflow')

    execute_file(cur,path_to_sql='./sql/ddl/create_schema.sql')
    execute_file(cur,path_to_sql='./sql/ddl/create_table.sql')

    cur.close()

def main():

    res=Fixer_data(
        api_key='c2115e94ed1079772c6e6650dfadb599',
        base='EUR',
        symbols=['BPI','USD','EUR','GBP'])

    print('trying to connect')

    cur=connect(
        host='postgres',
        database='airflow',
        user='airflow',
        password='airflow')

    res.insert_statement(cur)

    cur.close()