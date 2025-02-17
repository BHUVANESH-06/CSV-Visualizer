import psycopg2
from config import DB_CONFIG

def execute_query(query, params=None, fetch_one=False):
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute(query, params or ())

    result = None
    if fetch_one:  
        result = cursor.fetchone()  

    connection.commit()
    cursor.close()
    connection.close()
    
    return result  
