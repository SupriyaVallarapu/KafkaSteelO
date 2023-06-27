import mysql.connector
from faker import Faker
import random
import time

fake = Faker()

MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD = "localhost", "3306", "root", "mysql"

try:
    # Ask the user for the MySQL details
    MYSQL_HOST = input("Enter your MySQL host: ") or MYSQL_HOST
    MYSQL_PORT = input("Enter your MySQL port: ") or MYSQL_PORT
    MYSQL_DB_NAME = input("Enter your MySQL database name: ")
    MYSQL_USER = input("Enter your MySQL username: ") or MYSQL_USER
    MYSQL_PASSWORD = input("Enter your MySQL password: ") or MYSQL_PASSWORD

    # Connect to your MySQL DB
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Confirm successful connection by printing MySQL version
    cur.execute("SELECT VERSION();")
    version = cur.fetchone()
    print(f"Connected to MySQL version: {version[0]}")

    # Ask the user for the number of tables
    num_tables = int(input("Enter the number of tables you want to generate: "))

    for i in range(num_tables):
        table_name = f'test_data_{i}'

        # Create table if it does not exist
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            varchar_col VARCHAR(50),
            boolean_col BOOLEAN,
            float_col FLOAT
        )
        """)

    # Enter the infinite loop
    while True:
        for i in range(num_tables):
            table_name = f'test_data_{i}'

            for _ in range(10):
                # Insert a new row
                cur.execute(
                    f"INSERT INTO {table_name} (varchar_col, boolean_col, float_col) VALUES (%s, %s, %s)", 
                    (fake.name(), random.choice([True, False]), random.uniform(1.0, 100.0))
                )

                if random.choice([True, False]):
                    # Randomly update some rows
                    new_boolean = random.choice([True, False])
                    new_float = random.uniform(1.0, 100.0)
                    cur.execute(
                        f"UPDATE {table_name} SET boolean_col = %s, float_col = %s WHERE id = %s",
                        (new_boolean, new_float, random.randint(1, _+1))
                    )

                if random.choice([True, False]) and _ > 0:
                    # Randomly delete some rows
                    cur.execute(
                        f"DELETE FROM {table_name} WHERE id = %s", 
                        (random.randint(1, _),)
                    )

                # Commit the transaction
                conn.commit()

            # Add delay after each batch
            time.sleep(5)

    # Close communication with the database
    cur.close()
    conn.close()

except mysql.connector.Error as e:
    print(f"An error occurred with mysql.connector: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
