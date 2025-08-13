from src.py.database import Respository
from unittest import TestCase

db = Respository()

class Testing(TestCase):
    def setUp(self):
        db.add('task1', 'COMPLETE', '2020-12-05 12:55:10', 'description')
        db.add('task2', 'IN PROGRESS', '2026-01-13 23:59:59')
 
    def tearDown(self):
        db.delete_all()

    