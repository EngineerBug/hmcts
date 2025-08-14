# HMCTS Task Manager

## Frontend

### Running the Project

Execute the run.sh or run.bat scripts in the root of the project.

### Task Display

- If the status of a task is 'COMPLETE' the task will appear green.

## Backend

### Importing the Backend into a Project

from backend.backend import Database

backend = Database('database_name')

### Error Handling

All Database functions may return an optional 'errorMsg' field, that describes what went wrong.

### Database API

createTask(title: str, status: str, dueDateTime: 'YYYY-MM-DD hh:mm:ss', description: optional(str))

    -> {'isCreated':{1,0,-1}}

    isCreated==1 => success

    isCreated==0 => failure

    isCreated==-1 => an exception occurred, so if the row was created is unclear

getTask(id: int)

    -> {'idFound': {1,0,-1}, 'id': int, 'title': String, 'description': String, 'status': String, 'dueDateTime': 'YYYY-MM-DD hh:mm:ss'}

    idFound==1 => id does exist

    idFound==0 => id does NOT exist

    idFound==-1 => an exception occurred, so the if the row exists is unclear

getTasks()

    -> [{'id': int, 'title': String, 'description': String, 'status': String, 'dueDateTime': 'YYYY-MM-DD hh:mm:ss'}]

updateTaskStatus(id: int, newStatus: str)

    -> {'isUpdated':{1,0,-1}}

    isUpdated==1 => row was updated

    isUpdated==0 => row was not updated

    isUpdated==-1 => an exception occurred, so the if the row was updated is unclear

deleteTask(id: int)

    -> {'isDeleted':{1,0,-1}}

    isDeleted==1 => row was deleted

    isDeleted==0 => row was not deleted
    
    isDeleted==-1 => an exception occurred, so the if the row was deleted is unclear

### Testing

To test the backend project, run the test.sh or test.bat scripts in the root of the project.

Alternatively, run 'python -m unittest backend.test.test_backend' or 'python3 -m unittest backend.test.test_backend' in the command line.