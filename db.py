import psycopg2


conn = psycopg2.connect(
    user="postgres",
    password="lamy",
    host="127.0.0.1",
    port="5432",)
cursor = conn.cursor()
conn.autocommit = True
    
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
classes TEXT NOT NULL,
birthday TEXT,
gender TEXT,
image TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS log (
id SERIAL PRIMARY KEY,
key TEXT NOT NULL,
data TEXT NOT NULL,
clock TEXT NOT NULL,
image TEXT NOT NULL
)''')
#conn.commit()
 

def in_user(name,group,birthday,gender,image):
    cursor.execute('INSERT INTO Users(name,classes,birthday,gender,image) VALUES (%s,%s,%s,%s,%s)',(name,group,birthday,gender,image))
#in_user('ivan','FEBO','21.03.2005','M','132.jpg')
cursor.close()  # закрываем курсор
conn.close()    # закрываем подключение 