import cx_Oracle
from faker import Faker
import random
import time

fake = Faker()

ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN = "system", "oracle", "localhost:1521/orcl"

try:
    # Ask the user for the Oracle details
    ORACLE_USER = input("Enter your Oracle username: ") or ORACLE_USER
    ORACLE_PASSWORD = input("Enter your Oracle password: ") or ORACLE_PASSWORD
    ORACLE_DSN = input("Enter your Oracle DSN: ") or ORACLE_DSN

    # Connect to your Oracle DB
    conn = cx_Oracle.connect(ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Confirm successful connection by printing Oracle version
    cur.execute("SELECT * FROM v$version WHERE banner LIKE 'Oracle%'")
    version = cur.fetchone()
    print(f"Connected to Oracle version: {version[0]}")

    # Ask the user for the number of tables
    num_tables = int(input("Enter the number of tables you want to generate: "))

    for i in range(num_tables):
        table_name = f'test_data_{i}'

        # Create table if it does not exist
        cur.execute(f"""
        DECLARE
            v_count NUMBER;
        BEGIN
            SELECT COUNT(*) INTO v_count FROM user_tables WHERE table_name = UPPER('{table_name}');
            IF v_count = 0 THEN
                EXECUTE IMMEDIATE '
                CREATE TABLE {table_name} (
                    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    varchar_col VARCHAR2(50),
                    boolean_col NUMBER(1),
                    float_col FLOAT
                )';
            END IF;
        END;
        """)

    # Enter the infinite loop
    while True:
        for i in range(num_tables):
            table_name = f'test_data_{i}'

            for _ in range(10):
                # Insert a new row
                cur.execute(
                    f"INSERT INTO {table_name} (varchar_col, boolean_col, float_col) VALUES (:1, :2, :3)", 
                    (fake.name(), random.choice([0, 1]), random.uniform(1.0, 100.0))
                )

                if random.choice([True, False]):
                    # Randomly update some rows
                    new_boolean = random.choice([0, 1])
                    new_float = random.uniform(1.0, 100.0)
                    cur.execute(
                        f"UPDATE {table_name} SET boolean_col = :1, float_col = :2 WHERE id = :3",
                        (new_boolean, new_float, random.randint(1, _+1))
                    )

                if random.choice([True, False]) and _ > 0:
                    # Randomly delete some rows
                    cur.execute(
                        f"DELETE FROM {table_name} WHERE id = :1", 
                        (random.randint(1, _),)
                    )

                # Commit the transaction
                conn.commit()

            # Add delay after each batch
            time.sleep(5)

    # Close communication with the database
    cur.close()
    conn.close()

except cx_Oracle.Error as e:
    print(f"An error occurred with cx_Oracle: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
