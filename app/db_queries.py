import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def db_connection():
    conn = psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn


def db_create_table():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS phone_book
         (user_id SERIAL,
         firstname VARCHAR (50) NOT NULL,
         lastname VARCHAR (50) NOT NULL,
         phone_number VARCHAR (50) NOT NULL,
         age INT);''')

    conn.commit()
    conn.close()
    cur.close()


def db_add_user(parametrs):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute('''INSERT INTO phone_book (firstname, lastname, phone_number, age)
                VALUES (%s, %s, %s, %s);''',
                (parametrs.firstname, parametrs.lastname, parametrs.phone_number, parametrs.age))
    conn.commit()
    conn.close()
    cur.close()


def db_get_user(lastname):
    conn = db_connection()
    df = pd.read_sql(f"SELECT * FROM phone_book WHERE lastname='{lastname}'", con=conn)
    conn.close()
    return df
