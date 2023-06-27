import psycopg2
from psycopg2 import sql
from faker import Faker
import random
import time

fake = Faker()

POSTGRES_HOST,POSTGRES_PORT,POSTGRES_USER,POSTGRES_PASSWORD = "localhost","5432","postgres","postgres"

try:
    # Ask the user for the PostgreSQL details
    POSTGRES_HOST = input("Enter your PostgreSQL host: ") or POSTGRES_HOST
    POSTGRES_PORT = input("Enter your PostgreSQL port: ") or POSTGRES_PORT
    POSTGRES_DB_NAME = input("Enter your PostgreSQL database name: ")
    POSTGRES_SCHEMA = input("Enter your PostgreSQL schema: ")
    POSTGRES_USER = input("Enter your PostgreSQL username: ") or POSTGRES_USER
    POSTGRES_PASSWORD = input("Enter your PostgreSQL password: ") or POSTGRES_PASSWORD

    # Connect to your postgres DB
    conn = psycopg2.connect(
        dbname=POSTGRES_DB_NAME, 
        user=POSTGRES_USER, 
        password=POSTGRES_PASSWORD, 
        host=POSTGRES_HOST,
        port=POSTGRES_PORT)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Confirm successful connection by printing PostgreSQL version
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"Connected to PostgreSQL version: {version[0]}")

    # Ask the user for the number of tables
    num_tables = int(input("Enter the number of tables you want to generate: "))

    for i in range(num_tables):
        table_name = f'test_data_{i}'

        # Create table if it does not exist
        table_create = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}.{} (
            id serial PRIMARY KEY,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            varchar_col VARCHAR(50),
            boolean_col BOOLEAN,
            float_col FLOAT
        )
        """).format(sql.Identifier(POSTGRES_SCHEMA), sql.Identifier(table_name))

        cur.execute(table_create)

    # Enter the infinite loop
    while True:
        for i in range(num_tables):
            table_name = f'test_data_{i}'

            for _ in range(10):
                # Insert a new row
                cur.execute(
                    sql.SQL("INSERT INTO {}.{} (varchar_col, boolean_col, float_col) VALUES (%s, %s, %s)").format(sql.Identifier(POSTGRES_SCHEMA), sql.Identifier(table_name)), 
                    (fake.name(), random.choice([True, False]), random.uniform(1.0, 100.0))
                )

                if random.choice([True, False]):
                    # Randomly update some rows
                    new_boolean = random.choice([True, False])
                    new_float = random.uniform(1.0, 100.0)
                    cur.execute(
                        sql.SQL("UPDATE {}.{} SET boolean_col = %s, float_col = %s WHERE id = %s").format(sql.Identifier(POSTGRES_SCHEMA), sql.Identifier(table_name)),
                        (new_boolean, new_float, random.randint(1, _+1))
                    )

                if random.choice([True, False]) and _ > 0:
                    # Randomly delete some rows
                    cur.execute(
                        sql.SQL("DELETE FROM {}.{} WHERE id = %s").format(sql.Identifier(POSTGRES_SCHEMA), sql.Identifier(table_name)), 
                        (random.randint(1, _),)
                    )

                # Commit the transaction
                conn.commit()

            # Add delay after each batch
            time.sleep(5)

    # Close communication with the database
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print(f"An error occurred with psycopg2: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
