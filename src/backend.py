from flask import Flask, request
import logging

from src.py.database import Respository
from src.py.consts import FAILURE, UNKNOWN

api = Flask(__name__)
db = Respository()

log_format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename = "main.log",
                    level = logging.INFO,
                    encoding = 'utf-8',
                    format = log_format,)
logger = logging.getLogger()

# create task
@api.route('/create', methods=['POST'])
def create():
    json = request.getJson()
    if 'title' not in json:
        return {'errorMsg': 'failed to create, missing title'}, 404
    if 'status' not in json:
        return {'errorMsg': 'failed to create, missing status'}, 404
    if 'dueDateTime' not in json:
        return {'errorMsg': 'failed to create, missing dueDateTime'}, 404
    
    result = None
    if 'description' in json:
        db.createTask(json['title'], json['status'], json['dueDateTime'], json['description'])
    else:
        db.createTask(json['title'], json['status'], json['dueDateTime'])

    if result == None or 'errorMsg' in result:
        return {'errorMsg':result['errorMsg']}, 500
    return 201

# retrieve task by id
@api.route('/get_task/<int:id>', methods=['GET'])
def getTaskById(id):
    task = db.getTask(id)
    if task['idFound'] == FAILURE:
        return {'errorMsg': 'failed to get task'}, 404
    if task['idFound'] == UNKNOWN:
        return {'errorMsg': 'failed to get task'}, 500
    return task, 200

# retrieve all tasks
@api.route('/get_tasks', methods=['GET'])
def getTasks():
    tasks = db.getTasks()
    if 'errorMsg' in tasks:
        return {'errorMsg': 'failed to get tasks'}, 500
    return tasks, 200

# update the status of a task
@api.route('/update_status/<int:id>', methods=['PATCH', 'PUT'])
def updateStatus(id):
    newStatus = request.getJson()['status']
    if newStatus is None:
        return {'errorMsg': f'failed to update task, new \'status\' required as JSON'}, 404
    target = db.getTask(id)
    if target['idFound'] == FAILURE:
        return {'errorMsg': f'failed to update task, {id} not valid task'}, 404
    if target['idFound'] == UNKNOWN:
        return {'errorMsg': 'failed to update task'}, 500
    if 'errorMsg' in db.updateTaskStatus(id, newStatus):
        return {'errorMsg': 'failed to update task'}, 500
    return 204

# delete a task
@api.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    target = db.getTask(id)
    if target['idFound'] == FAILURE:
        return {'errorMsg': f'failed to delete task, {id} not valid task'}, 404
    if target['idFound'] == UNKNOWN or 'errorMsg' in db.deleteTask(id):
        return {'errorMsg': 'failed to delete task'}, 500
    return 204

# frontend page (Create, view, update, and delete tasks in a user friendly manner)
@api.route('/', methods=['GET'])
def main():
    pass

if __name__ == '__main__':
    api.run(host='127.0.0.1', port='8080')