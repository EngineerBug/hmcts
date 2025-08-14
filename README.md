# HMCTS Task Manager

## Frontend

### Task Display

- If the status of a task is 'COMPLETE' the task will appear green.

## Backend

### importing the backend into a project

from backend.backend import Database

backend = Database('database_name')

### Error Handling

All Database functions may return an optional 'errorMsg' field, that describes what went wrong.

### Database API

createTask(title: str, status: str, dueDateTime: 'YYYY-MM-DD hh:mm:ss', description: optional(str))
    -> {'status':{1,0,-1}}
    status==1 => success
    status==0 => failure
    idFound==-1 => an exception occurred, so if the row was created is unclear

getTask(id: int)
    -> {'idFound': {1,0,-1}, 'id': int, 'title': String, 'description': String, 'status': String, 'dueDateTime': DateTime}
    idFound==1 => id does exist
    idFound==0 => id does NOT exist
    idFound==-1 => an exception occurred, so the if the row exists is unclear

getTasks()
    -> [{'id': int, 'title': String, 'description': String, 'status': String, 'dueDateTime': DateTime}]

updateTaskStatus(id: int, newStatus: str)
    -> {'status':{1,0,-1}}
    idFound==1 => row was updated
    idFound==0 => row was not updated
    idFound==-1 => an exception occurred, so the if the row was updated is unclear

deleteTask(id: int)
    -> {'status':{1,0,-1}}
    idFound==1 => row was deleted
    idFound==0 => row was not deleted
    idFound==-1 => an exception occurred, so the if the row was deleted is unclear