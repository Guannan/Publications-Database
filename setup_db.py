import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('publications.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create Authors table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        AuthorID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Affiliation TEXT
    )
''')

# Create Publications table with updated fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Publications (
        PublicationID INTEGER PRIMARY KEY,
        Title TEXT NOT NULL,
        Year INTEGER,
        Journal TEXT,
        Summary TEXT,
        Methodologies TEXT,
        Outcomes TEXT,
        DataSources TEXT,
        ResearchQuestions TEXT
    )
''')

# Create Author_Publications link table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Author_Publications (
        AuthorID INTEGER,
        PublicationID INTEGER,
        FOREIGN KEY (AuthorID) REFERENCES Authors (AuthorID),
        FOREIGN KEY (PublicationID) REFERENCES Publications (PublicationID)
    )
''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
