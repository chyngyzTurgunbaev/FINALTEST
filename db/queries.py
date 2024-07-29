class Queries:
    CREATE_SURVEY_TABLE = """CREATE TABLE IF NOT EXISTS survey(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    age INTEGER,
    occupation TEXT,
    salary INTEGER
    )
    """
