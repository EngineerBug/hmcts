from sqlite3 import connect
from datetime import datetime
from backend.py.consts import SUCCESS, FAILURE, UNKNOWN, DATE_TIME_FORMAT, ERROR_MSG_NAME

class Database:
    def __init__(self, dbName):
        self.database = f'{dbName}.db' 
        self.make()

    def make(self):
        with connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                dueDateTime DATETIME NOT NULL
            )''')
            connection.commit()

    # create task
    def createTask(self, title, status, dueDateTime, description=''):
        if title == '' or title is None:
            return {'status':FAILURE, ERROR_MSG_NAME:'failed to create, title was empty'}
        if status == '' or status is None:
            return {'status':FAILURE, ERROR_MSG_NAME:'failed to create, status was empty'}
        if dueDateTime == '' or dueDateTime is None:
            return {'status':FAILURE, ERROR_MSG_NAME:'failed to create, date/time was empty'}
        try:
            datetime.strptime(dueDateTime, DATE_TIME_FORMAT)
        except ValueError:
            return {'status':FAILURE, ERROR_MSG_NAME:f'dueDateTime format should be {DATE_TIME_FORMAT}'}
        
        with connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute('insert into Task (title, description, status, dueDateTime) values (?, ?, ?, ?)', (title, description, status, dueDateTime))
            connection.commit()
            return {'status':SUCCESS}
        return {'status':UNKNOWN, ERROR_MSG_NAME:f'failed to add task with title {title}'}

    # retrieve task by id
    # {'idFound': {1, 0, -1}, 'id': int, 'title': String, 'description': String, 'status': String, 'dueDateTime': DateTime}
    def getTask(self, id):
        with connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute('select * from Task where id=?', (id,))
            row = cursor.fetchone()
            if row == None:
                return {'idFound':FAILURE, ERROR_MSG_NAME:f'id {id} not found in Tasks'}
            return {'idFound':SUCCESS, 'id':row[0], 'title':row[1], 'description':row[2], 'status':row[3], 'dueDateTime':datetime.strptime(row[4], DATE_TIME_FORMAT)}
        return {'idFound':UNKNOWN, ERROR_MSG_NAME:f'failed to get task with id {id}'}

    # retrieve all tasks
    # [{'id': int, 'title': String, 'description': String, 'status': String, 'dueDateTime': DateTime}]
    def getTasks(self):
        with connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute('select * from Task')
            rows = cursor.fetchall()
            return [{'id':row[0], 'title':row[1], 'description':row[2], 'status':row[3], 'dueDateTime':datetime.strptime(row[4], DATE_TIME_FORMAT)} for row in rows]
        return {ERROR_MSG_NAME:'get task action failed'}

    # update the status of a task
    def updateTaskStatus(self, id, newStatus):
        if newStatus == '' or newStatus is None:
            return {'status': FAILURE, ERROR_MSG_NAME:'did not update, missing status'}
        
        with connect(self.database) as connection:
            cursor = connection.cursor()

            cursor.execute('select count(id) from Task where id=?', (id,))
            if cursor.fetchone()[0] == 0:
                return {'status': FAILURE, ERROR_MSG_NAME:'did not update, invalid id'}
            
            cursor.execute('update Task set status=? where id=?', (newStatus, id))
            connection.commit()
            return {'status': SUCCESS}
        return {'status': UNKNOWN, ERROR_MSG_NAME:f'failed to update task with id {id}'}

    # delete a task
    def deleteTask(self, id):
        with connect(self.database) as connection:
            cursor = connection.cursor()

            cursor.execute('select count(id) from Task where id=?', (id,))
            if cursor.fetchone()[0] == 0:
                return {'status':FAILURE, ERROR_MSG_NAME:'did not delete, invalid id'}
            
            cursor.execute('delete from Task where id=?', (id,))
            return {'status': SUCCESS}
        return {'status': UNKNOWN, ERROR_MSG_NAME:f'failed to delete task with id {id}'}