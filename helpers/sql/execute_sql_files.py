import psycopg2
import logging

def connect(host,database,user,password):
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)
    
    conn.autocommit = True
    
    cur = conn.cursor()
    
    return cur


def execute_file(cur,path_to_sql):
    
    cur.execute(open(path_to_sql, "r").read())
    
    logging.info('executing: {path_to_sql}')