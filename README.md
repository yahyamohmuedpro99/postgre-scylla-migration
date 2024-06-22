# PostgreSQL to ScyllaDB Migration Script
This script migrates data from PostgreSQL to ScyllaDB using Python, psycopg2 for PostgreSQL connectivity, and Cassandra's Python driver for ScyllaDB.
## Purpose
    The purpose of this script is to transfer data from PostgreSQL tables to corresponding tables in ScyllaDB. It handles the extraction of data from PostgreSQL , and insertion into ScyllaDB tables.

## Features
    - Connects to PostgreSQL using psycopg2 to fetch data from specified tables.
    - Connects to ScyllaDB using Cassandra's Cluster object to insert data into corresponding tables.
    - Supports migration of multiple tables from PostgreSQL to ScyllaDB in a single run.
    - Outputs migration success messages for each table migrated.


## how to use ? 
    - clone the repo and open the dir    
    - docker compose up 
    - python migrate.py (before run you need to change the host ips to what you have on your machine you can use this command down to get your ips )

### command to know the ip of spcific container 
`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id_or_name>`