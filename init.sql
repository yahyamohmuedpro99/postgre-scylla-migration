CREATE TABLE table1 (
    id SERIAL PRIMARY KEY,
    column1 TEXT,
    column2 TEXT
);

CREATE TABLE table2 (
    id SERIAL PRIMARY KEY,
    column1 TEXT,
    column2 TEXT
);

-- mock db to test with 
INSERT INTO table1 (column1, column2)
VALUES 
('This is a sample text for column 1.', 'This is some data for column 2 in table 1.'),
('Here''s another example of text content.', 'This is another row with some information.'),
('Text data can vary in length and format.', 'Text content can be descriptive or concise.'),
('Lorem ipsum dolor sit amet, consectetur...', 'Text can also include placeholders like lorem ipsum.');

INSERT INTO table2 (column1, column2)
VALUES 
('This is some data for table 2, column 1.', 'This is another table with sample content.'),
('Text content can be used for various purposes.', 'Text can be used for storing descriptions, notes, or any relevant information.'),
('Each row represents a unique data point.', 'Data can be structured or unstructured depending on the use case.'),
('Text fields allow for flexibility in data storage.', ''),
('Database tables help organize information.', 'Text data can be combined with other data types for comprehensive analysis.');
