import sqlite3
from timeit import default_timer as timer
from datetime import datetime

from pydriller import Repository
from git import Repo

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

    cursor.execute("DROP TABLE IF EXISTS file_changes;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_changes (
        id TEXT,
        path TEXT,
        insertions INTEGER,
        deletions INTEGER,
        PRIMARY KEY (id, path)
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
    print(f"[PyDriller] extracting {path} between {since} - {to}...")
    print(f"[PyDriller] NOT INSERTING FILE CHANGES.")
    repository = Repository(path, since=since, to=to)

    connection = sqlite3.connect(f"db/pydriller_extract.db")
    create_database(connection)
    cursor = connection.cursor()

    start_t = timer()
    for commit in repository.traverse_commits():
        row = (commit.hash, commit.author.name, commit.committer_date)
        cursor.execute("INSERT INTO commits VALUES (?, ?, ?)", row)
    end_t = timer()
    print("Time: ", end_t - start_t)

    connection.commit()
    dump_database_stats(connection)
    connection.close()


def extract_repo_with_git_python(path: str, since: datetime, to: datetime):
    print(f"[GitPython] extracting {path} between {since} - {to}...")
    repository = Repo(path)

    connection = sqlite3.connect(f"db/gitpython_extract.db")
    create_database(connection)
    cursor = connection.cursor()

    start_t = timer()
    for commit in repository.iter_commits(since=since, until=to):
        row = (commit.hexsha, commit.author.name, commit.committed_datetime)
        cursor.execute("INSERT INTO commits VALUES (?, ?, ?)", row)

        for filepath, stats in commit.stats.files.items():
            row = (commit.hexsha, filepath, stats['insertions'], stats['deletions'])
            cursor.execute("INSERT INTO file_changes VALUES (?, ?, ?, ?)", row)
    end_t = timer()
    print("Time: ", end_t - start_t)

    connection.commit()
    dump_database_stats(connection)
    connection.close()


t1 = datetime(2010, 1, 1)
t2 = datetime(2020, 1, 1)
extract_repo_with_pydriller("./repos/rails_full_clone", t1, t2)
extract_repo_with_git_python("./repos/rails_full_clone", t1, t2)
