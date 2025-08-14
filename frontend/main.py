from flask import Flask, request, render_template
import logging

from backend.backend import Database
from backend.py.consts import FAILURE, UNKNOWN

app = Flask(__name__)
db = Database('main')

log_format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename = "main.log",
                    level = logging.INFO,
                    encoding = 'utf-8',
                    format = log_format,)
logger = logging.getLogger()

# frontend page (Create, view, update, and delete tasks in a user friendly manner)
@app.route('/', methods=['GET'])
def main():
    tasks = db.getTasks()
    return render_template('main.html', tasks=tasks)

# create task
@app.route('/create', methods=['POST'])
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

    if result == None:
        return {'errorMsg':'did not create, something went wrong'}, 500
    elif result['status'] == FAILURE:
        return {'errorMsg':result['errorMsg']}, 404
    elif result['status'] == UNKNOWN:
        return {'errorMsg':result['errorMsg']}, 500
        
    return 201

# retrieve task by id
@app.route('/get_task/<int:id>', methods=['GET'])
def getTaskById(id):
    task = db.getTask(id)
    if task['idFound'] == FAILURE:
        return {'errorMsg': 'failed to get task, invalid id'}, 404
    if task['idFound'] == UNKNOWN:
        return {'errorMsg': 'failed to get task, internal error'}, 500
    return task, 200

# retrieve all tasks
@app.route('/get_tasks', methods=['GET'])
def getTasks():
    tasks = db.getTasks()
    if 'errorMsg' in tasks:
        return {'errorMsg': 'failed to get tasks'}, 500
    return tasks, 200

# update the status of a task
@app.route('/update_status/<int:id>', methods=['PATCH', 'PUT'])
def updateStatus(id):
    result = db.updateTaskStatus(id, request.getJson()['status'])
    if 'errorMsg' in result:
        return {'errorMsg': result['errorMsg']}, 404
    return 204

# delete a task
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    result = db.deleteTask(id)
    if 'errorMsg' in result:
        return {'errorMsg': result['errorMsg']}, 404
    return 204

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080')