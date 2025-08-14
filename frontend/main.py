from flask import Flask, request, render_template, flash, redirect
from secrets import token_hex
import logging

from backend.backend import Database
from backend.py.consts import FAILURE, SUCCESS, UNKNOWN

app = Flask(__name__)
app.secret_key = token_hex(32)
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
    if result['status'] == SUCCESS:
        flash(f'task successfully created', 'success')
    else:
        flash(result['errorMsg'], 'failure')
    return redirect('/')

# update the status of a task
@app.route('/update_status/<int:id>', methods=['POST', 'PATCH', 'PUT'])
def updateStatus(id):
    result = db.updateTaskStatus(id, request.form['newStatus'])
    if 'errorMsg' in result:
        flash(result['errorMsg'], 'failure')
    else:
        flash(f'task successfully updated', 'success')
    return redirect('/')

# delete a task
@app.route('/delete/<int:id>', methods=['POST', 'DELETE'])
def delete(id):
    result = db.deleteTask(id)
    if 'errorMsg' in result:
        flash(result['errorMsg'], 'failure')
    else:
        flash(f'task successfully deleted', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port='8080')