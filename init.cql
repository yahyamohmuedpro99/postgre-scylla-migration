CREATE KEYSPACE initdb WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};

USE initdb;

CREATE TABLE table1 (
    id int PRIMARY KEY,
    column1 text,
    column2 text
);

CREATE TABLE table2 (
    id int PRIMARY KEY,
    column1 text,
    column2 text
);

