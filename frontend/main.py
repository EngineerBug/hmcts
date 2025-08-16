from flask import Flask, request, render_template, flash, redirect
from secrets import token_hex
import logging

from backend.backend import Database
from backend.consts import ERROR_MSG_NAME

# Create the app
app = Flask(__name__)

# So the flash messages can be sent
app.secret_key = token_hex(32)

# Create the backend
db = Database('main')

# Logging setup
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
    logger.info(f'created result: {result}')

    # return the appropriate response
    if ERROR_MSG_NAME in result:
        flash(result[ERROR_MSG_NAME], 'failure')
    else:
        flash(f'task successfully created', 'success')
    return redirect('/')

# update the status of a task
@app.route('/update_status/<int:id>', methods=['POST', 'PATCH', 'PUT'])
def updateStatus(id):
    result = db.updateTaskStatus(id, request.form['newStatus'])
    if ERROR_MSG_NAME in result:
        flash(result[ERROR_MSG_NAME], 'failure')
    else:
        flash(f'task successfully updated', 'success')
    return redirect('/')

# delete a task
@app.route('/delete/<int:id>', methods=['POST', 'DELETE'])
def delete(id):
    result = db.deleteTask(id)
    if ERROR_MSG_NAME in result:
        flash(result[ERROR_MSG_NAME], 'failure')
    else:
        flash(f'task successfully deleted', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080')