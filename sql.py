import sqlite3

# Connect to sqlite
connection = sqlite3.connect("student.db")

# Create a cursor object to insert, create, and retrieve data
cursor = connection.cursor()

# Create the table if it doesn't already exist
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25), 
    SUBJECT VARCHAR(25),
    BRANCH VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)

# Insert five records into the STUDENT table with B.Tech subjects
insert_query = """
INSERT INTO STUDENT (NAME, SUBJECT, BRANCH, MARKS)
VALUES 
    ('Praveen', 'DM', 'CSE', 85),
    ('Ashwin', 'SE', 'CSE', 90),
    ('SaiPavan', 'OS', 'EEE', 88),
    ('Akhil', 'COA', 'MECH', 75),
    ('SA', 'COSM', 'CIVIL', 92);
"""
cursor.execute(insert_query)

print("Records inserted successfully!")


data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

# Commit the transaction and close the connection
connection.commit()
connection.close()
