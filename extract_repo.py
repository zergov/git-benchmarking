import sqlite3

def create_database(filename: str):
    connection = sqlite3.connect(filename)

    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS commits;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id TEXT PRIMARY KEY,
        author TEXT,
        committer_date INTEGER
    );
    """)

    connection.commit()
    connection.close()


create_database("db/testing.db")
