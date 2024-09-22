import sqlite3
from datetime import datetime

from pydriller import Repository

def create_database(connection: sqlite3.Connection):
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


def dump_database_stats(connection: sqlite3.Connection):
    cursor = connection.cursor()
    stats = {
        "commit_count": cursor.execute("SELECT count(*) FROM commits;").fetchone()[0],
    }
    print(stats)


def extract_repo_with_pydriller(path: str, since: datetime, to: datetime):
    repository = Repository(path, since=since, to=to)

    connection = sqlite3.connect(f"db/pydriller_extract.db")
    create_database(connection)
    cursor = connection.cursor()

    for commit in repository.traverse_commits():
        row = (commit.hash, commit.author.name, commit.committer_date)
        cursor.execute("INSERT INTO commits VALUES (?, ?, ?)", row)

    connection.commit()
    dump_database_stats(connection)
    connection.close()


t1 = datetime(2010, 1, 1)
t2 = datetime(2020, 1, 1)
extract_repo_with_pydriller("./repos/rails_full_clone", t1, t2)
