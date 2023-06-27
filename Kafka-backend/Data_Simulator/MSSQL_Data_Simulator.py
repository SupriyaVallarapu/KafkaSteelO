import pyodbc
from faker import Faker
import random
import time

fake = Faker()

MSSQL_SERVER, MSSQL_PORT, MSSQL_USER, MSSQL_PASSWORD = "localhost", "1433", "sa", "password"

try:
    # Ask the user for the MSSQL details
    MSSQL_SERVER = input("Enter your MSSQL server: ") or MSSQL_SERVER
    MSSQL_PORT = input("Enter your MSSQL port: ") or MSSQL_PORT
    MSSQL_DB_NAME = input("Enter your MSSQL database name: ")
    MSSQL_USER = input("Enter your MSSQL username: ") or MSSQL_USER
    MSSQL_PASSWORD = input("Enter your MSSQL password: ") or MSSQL_PASSWORD

    # Connect to your MSSQL DB
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={MSSQL_SERVER},{MSSQL_PORT};'
        f'DATABASE={MSSQL_DB_NAME};'
        f'UID={MSSQL_USER};'
        f'PWD={MSSQL_PASSWORD}'
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Confirm successful connection by printing MSSQL version
    cur.execute("SELECT @@VERSION")
    version = cur.fetchone()
    print(f"Connected to MSSQL version: {version[0]}")

    # Ask the user for the number of tables
    num_tables = int(input("Enter the number of tables you want to generate: "))

    for i in range(num_tables):
        table_name = f'dbo.test_data_{i}'

        # Create table if it does not exist
        cur.execute(f"""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
        CREATE TABLE {table_name} (
            id INT IDENTITY(1,1) PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            varchar_col VARCHAR(50),
            boolean_col BIT,
            float_col FLOAT
        )
        """)

    # Enter the infinite loop
    while True:
        for i in range(num_tables):
            table_name = f'dbo.test_data_{i}'

            for _ in range(10):
                # Insert a new row
                cur.execute(
                    f"INSERT INTO {table_name} (varchar_col, boolean_col, float_col) VALUES (?, ?, ?)", 
                    (fake.name(), random.choice([True, False]), random.uniform(1.0, 100.0))
                )

                if random.choice([True, False]):
                    # Randomly update some rows
                    new_boolean = random.choice([True, False])
                    new_float = random.uniform(1.0, 100.0)
                    cur.execute(
                        f"UPDATE {table_name} SET boolean_col = ?, float_col = ? WHERE id = ?",
                        (new_boolean, new_float, random.randint(1, _+1))
                    )

                if random.choice([True, False]) and _ > 0:
                    # Randomly delete some rows
                    cur.execute(
                        f"DELETE FROM {table_name} WHERE id = ?", 
                        (random.randint(1, _),)
                    )

                # Commit the transaction
                conn.commit()

            # Add delay after each batch
            time.sleep(5)

    # Close communication with the database
    cur.close()
    conn.close()

except pyodbc.Error as e:
    print(f"An error occurred with pyodbc: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
