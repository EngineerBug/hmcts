from flask import Flask, request, render_template
import logging

from backend.backend import Database
from backend.py.consts import FAILURE, UNKNOWN

app = Flask(__name__)
db = Database('main')

log_format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename = 'main.log',
                    level = logging.INFO,
                    encoding = 'utf-8',
                    format = log_format,)
logger = logging.getLogger()

# frontend page; create, view, update, and delete tasks in a user friendly manner
@app.route('/', methods=['GET'])
def main():
    tasks = db.getTasks()
    return render_template('main.html', tasks=tasks)

# create task
@app.route('/create', methods=['POST'])
def create():
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    datetime = request.form['datetime']

    # convert from HTML format (YYYY-MM-DDThh:mm) to SQL format (YYYY-MM-DD hh:mm:ss)
    logger.info(f'datetime recived by create: {datetime}')
    parsedDatetime = datetime.replace('T', ' ') + ':00'
    logger.info(f'datetime after parsed by create: {parsedDatetime}')

    # perform the backend function call
    result = db.createTask(title, status, parsedDatetime, description)
    logger.info(f'create result: {result}')

    # return the appropriate response
    if result['status'] == FAILURE:
        return {'errorMsg':result['errorMsg']}, 404
    elif result['status'] == UNKNOWN:
        return {'errorMsg':result['errorMsg']}, 500
    return {}, 201

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
@app.route('/update_status/<int:id>', methods=['POST', 'PATCH', 'PUT'])
def updateStatus(id):
    result = db.updateTaskStatus(id, request.form['newStatus'])
    if 'errorMsg' in result:
        return {'errorMsg': result['errorMsg']}, 404
    return {}, 204

# delete a task
@app.route('/delete/<int:id>', methods=['POST', 'DELETE'])
def delete(id):
    result = db.deleteTask(id)
    if 'errorMsg' in result:
        return {'errorMsg': result['errorMsg']}, 404
    return {}, 204

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port='8080')