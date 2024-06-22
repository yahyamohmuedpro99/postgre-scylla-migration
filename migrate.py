import psycopg2
from cassandra.cluster import Cluster

# ------------------ connection of db's --------------------
# ----------------------------------------------------------
def get_postgres_connection(database, user, password, host, port):
    return psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

def get_scylla_connection(contact_points, keyspace):
    return Cluster(contact_points).connect(keyspace)

# ----------------------------------------------------------
# ----------------------------------------------------------

def fetch_data_from_postgres(pg_cursor, table_name):
    pg_cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in pg_cursor.description]
    rows = pg_cursor.fetchall()
    return columns, rows

def insert_data_into_scylla(session, table_name, columns, rows):
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})"
    # prepared = session.prepare(insert_query)
    for row in rows:
        session.execute(insert_query, row)

def migrate_table(pg_cursor, scylla_session, table_name):
    columns, rows = fetch_data_from_postgres(pg_cursor, table_name)
    insert_data_into_scylla(scylla_session, table_name, columns, rows)
    print(f"Data from table {table_name} migrated successfully.")



def main():
    # PostgreSQL connection parameters
    pg_config = {
        'database': 'initdb',
        'user': 'postgres',
        'password': 'postgres',
        'host': '172.22.0.2',  
        'port': '5432'
    }

    # ScyllaDB connection parameters
    scylla_config = {
        'contact_points': ['172.23.0.2', '172.23.0.4', '172.23.0.3'], 
        'keyspace': 'initdb'
    }

    # Tables to migrate
    tables = ['table1', 'table2']  

    # Connect to PostgreSQL
    pg_conn = get_postgres_connection(**pg_config)
    pg_cursor = pg_conn.cursor()

    # Connect to ScyllaDB
    scylla_session = get_scylla_connection(scylla_config['contact_points'], scylla_config['keyspace'])

    # Migrate each table
    for table in tables:
        migrate_table(pg_cursor, scylla_session, table)

    # Close connections
    pg_cursor.close()
    pg_conn.close()
    scylla_session.shutdown()

if __name__ == "__main__":
    main()
