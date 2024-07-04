import json
import time
import psycopg2
from cassandra.cluster import Cluster
import uuid
from cassandra.query import PreparedStatement
from datetime import datetime

import logging
from tables import table_names, pg_config, column_mapping, scylla_config

logging.basicConfig(level=logging.INFO)


# ---------------------------------------------
# ------------- DB's connection ---------------
# ---------------------------------------------
def get_postgres_connection(database, user, password, host, port):
    return psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

def get_scylla_connection(contact_points, keyspace, max_retries=3):
    cluster = None
    for i in range(max_retries):
        try:
            cluster = Cluster(contact_points)
            session = cluster.connect(keyspace)
            logging.info(f"Connected to ScyllaDB cluster at {contact_points}")
            return session
        except Exception as e:
            logging.error(f"Error connecting to ScyllaDB on attempt {i + 1}: {e}")
            if i < max_retries - 1:
                time.sleep(2 ** i)  
            else:
                raise

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

# ---------------------------------------------
# ------------- get and insert data -----------
# ---------------------------------------------
def fetch_data_from_postgres(pg_cursor, table_name):
    pg_cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in pg_cursor.description]
    rows = pg_cursor.fetchall()
    return columns, rows

def prepare_and_insert_data_into_scylla(session, table_name: str, columns: list, rows: list, column_mapping: dict):
    scylla_columns = [column_mapping.get(col, col) for col in columns]

    insert_query = f"INSERT INTO {table_name} ({', '.join(scylla_columns)}) VALUES ({', '.join(['?' for _ in scylla_columns])})"
    prepared = session.prepare(insert_query)

    for row in rows:
        row_data = []
        for i, value in enumerate(row):
            column = columns[i]
            if value is None:
                row_data.append(None) 
            elif isinstance(value, uuid.UUID):
                row_data.append(value)
            elif isinstance(value, str) and len(value) == 36:
                try:
                    row_data.append(uuid.UUID(value))
                except ValueError:
                    row_data.append(value)
            elif isinstance(value, datetime):
                row_data.append(value)
            elif isinstance(value, list) or isinstance(value, dict):
                row_data.append(json.dumps(value))  
            elif column == 'max_sequencers':
                try:
                    row_data.append(int(value))
                except (ValueError, TypeError) as e:
                    logging.error(f"Error converting value '{value}' to int for column '{column}': {e}")
                    row_data.append(0)  
            else:
                row_data.append(value)
        
        logging.info(f"Row data to insert: {row_data}")
        try:
            session.execute(prepared, row_data)
            logging.info("Data inserted successfully.")
        except Exception as e:
            logging.error(f"Error inserting data into ScyllaDB: {e}")

def migrate_table(pg_cursor, scylla_session, table_name, column_mapping):
    columns, rows = fetch_data_from_postgres(pg_cursor, table_name)
    prepare_and_insert_data_into_scylla(scylla_session, table_name, columns, rows, column_mapping)
    print(f"Data from table {table_name} migrated successfully.")

def main():

    tables = table_names

    pg_conn = get_postgres_connection(**pg_config)
    pg_cursor = pg_conn.cursor()
    scylla_session = get_scylla_connection(scylla_config['contact_points'], scylla_config['keyspace'])

    for table in tables:
        migrate_table(pg_cursor, scylla_session, table, column_mapping.get(table, {}))

    pg_cursor.close()
    pg_conn.close()
    scylla_session.shutdown()

if __name__ == "__main__":
    main()
