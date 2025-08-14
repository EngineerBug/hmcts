from backend.backend import Database
from backend.py.consts import SUCCESS, FAILURE, ERROR_MSG_NAME
from sqlite3 import connect
from unittest import TestCase
from datetime import datetime

TEST_DB_NAME = 'test'
DB = TEST_DB_NAME + '.db'

class Testing(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database(TEST_DB_NAME)
        cls.connection = connect(DB)
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        self.db.createTask('task1', 'COMPLETE', '2020-12-05 12:55:10', 'description')
        self.db.createTask('task2', 'IN PROGRESS', '2026-01-13 23:59:59')

    def tearDown(self):
        self.cursor.execute(f'delete from Task')
        self.connection.commit()

    def testAdd_success(self):
        # given
        creation = self.db.createTask('task3', 'NOT STARTED', '2026-12-05 09:45:00', 'asgfagrgesdvcwadh')

        # when
        self.cursor.execute('select * from Task where title=\'task3\'')
        result = self.cursor.fetchall()

        # then
        self.assertEqual(creation['status'], SUCCESS)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'task3')
        self.assertEqual(result[0][2], 'asgfagrgesdvcwadh')
        self.assertEqual(result[0][3], 'NOT STARTED')
        self.assertEqual(result[0][4], '2026-12-05 09:45:00')

    def testAdd_emptyTitle(self):
        # given
        # when
        result = self.db.createTask('', 'NOT STARTED', '2026-12-05 09:45:00', 'asgfagrgesdvcwadh')

        # then
        self.assertEqual(result['status'], FAILURE)

    def testAdd_noneTitle(self):
        # given
        # when
        result = self.db.createTask(None, 'NOT STARTED', '2026-12-05 09:45:00', 'asgfagrgesdvcwadh')

        # then
        self.assertEqual(result[ERROR_MSG_NAME], 'failed to create, title was empty')

    def testAdd_emptyStatus(self):
        # given
        # when
        result = self.db.createTask('task3', '', '2026-12-05 09:45:00', 'asgfagrgesdvcwadh')

        # then
        self.assertEqual(result[ERROR_MSG_NAME], 'failed to create, status was empty')

    def testAdd_noneStatus(self):
        # given
        # when
        result = self.db.createTask('task3', None, '2026-12-05 09:45:00', 'asgfagrgesdvcwadh')

        # then
        self.assertEqual(result[ERROR_MSG_NAME], 'failed to create, status was empty')

    def testAdd_emptyDueDateTime(self):
        # given
        # when
        result = self.db.createTask('task3', 'NOT STARTED', '', 'asgfagrgesdvcwadh')

        # then
        self.assertEqual(result[ERROR_MSG_NAME], 'failed to create, date/time was empty')

    def testAdd_noneDueDateTime(self):
        # given
        # when
        result = self.db.createTask('task3', 'NOT STARTED', None, 'asgfagrgesdvcwadh')

        # then
        self.assertEqual(result[ERROR_MSG_NAME], 'failed to create, date/time was empty')

    def testAdd_wrongDateTimeFormat(self):
        # given

        # when
        result = self.db.createTask('task3', 'NOT STARTED', 'INVALID', 'asgfagrgesdvcwadh')

        # then
        self.assertEqual(result['status'], FAILURE)

    def testGetById_success(self):
        # given
        self.cursor.execute('select * from Task where title=\'task1\'')
        id = self.cursor.fetchone()[0]

        # when
        result = self.db.getTask(id)

        # then
        self.assertEqual(result['idFound'], SUCCESS)
        self.assertEqual(result['title'], 'task1')
        self.assertEqual(result['description'], 'description')
        self.assertEqual(result['status'], 'COMPLETE')
        self.assertEqual(result['dueDateTime'], '2020-12-05 12:55:10')

    def testGetById_invalidId(self):
        # given
        self.cursor.execute('delete from Task')

        # when
        result = self.db.getTask(1)

        # then
        self.assertEqual(result[ERROR_MSG_NAME], 'id 1 not found in Tasks')
        self.assertEqual(result['idFound'], FAILURE)

    def testRetriveAllTasks_success(self):
        # given

        # when
        results = self.db.getTasks()
        
        # then
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'task1')
        self.assertEqual(results[1]['title'], 'task2')

    def testRetriveAllTasks_empty(self):
        # given
        self.cursor.execute(f'delete from Task')
        self.connection.commit()

        # when
        results = self.db.getTasks()
        
        # then
        self.assertEqual(len(results), 0)

    def testUpdate_success(self):
        # given
        self.cursor.execute('select id from Task where title=\'task2\'')
        id = self.cursor.fetchone()[0]

        # when
        result = self.db.updateTaskStatus(id, 'COMPLETE')
        row = self.db.getTask(id)
        
        # then
        self.assertEqual(result['status'], SUCCESS)
        self.assertEqual(row['title'], 'task2')
        self.assertEqual(row['description'], '')
        self.assertEqual(row['status'], 'COMPLETE')
        self.assertEqual(row['dueDateTime'], '2026-12-05 09:45:00')

    def testUpdate_emptyStatus(self):
        # given
        self.cursor.execute('select id from Task where title=\'task2\'')
        id = self.cursor.fetchone()[0]

        # when
        result = self.db.updateTaskStatus(id, '')
        row = self.db.getTask(id)

        # then
        self.assertEqual(row['status'], 'IN PROGRESS')
        self.assertEqual(result['status'], FAILURE)

    def testUpdate_invalidId(self):
        # given
        self.cursor.execute(f'delete from Task')
        self.connection.commit()

        # when
        result = self.db.updateTaskStatus(1, 'COMPLETE')

        # then
        self.assertEqual(result['status'], FAILURE)

    def testDelete_success(self):
        # given
        self.cursor.execute('select * from Task where title=\'task2\'')
        id = self.cursor.fetchone()[0]

        # when
        result = self.db.deleteTask(id)
        row = self.db.getTask(id)
        
        # then
        self.assertEqual(result['status'], SUCCESS)
        self.assertEqual(row['idFound'], FAILURE)

    def testDelete_invalidId(self):
        # given
        self.cursor.execute(f'delete from Task')
        self.connection.commit()

        # when
        result = self.db.deleteTask(1)

        # then
        self.assertEqual(result['status'], FAILURE)