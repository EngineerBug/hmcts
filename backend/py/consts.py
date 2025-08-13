SUCCESS = 1
FAILURE = 0
UNKNOWN = -1
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CREATE_TASK_TABLE_SQL_STRING = '''CREATE TABLE IF NOT EXISTS Task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        dueDateTime DATETIME NOT NULL
    )'''

ERROR_MSG_NAME = 'errorMsg'