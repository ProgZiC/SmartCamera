import psycopg2

conn = psycopg2.connect(dbname="postgres", user="postgres", password="lamy", host="127.0.0.1")
cursor = conn.cursor()
conn.autocommit = True
    
def enter():

    sql1 = 'CREATE DATABASE Humans'
    cursor.execute(sql1)
 
 
cursor.close()  # закрываем курсор
conn.close()    # закрываем подключение 