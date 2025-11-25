from fastapi import FastAPI
from repository import UserRepository, TaskRepository
from models import AddUserModel, AddTaskModel, ChangeTaskModel

app = FastAPI()

task_repo = TaskRepository('test.db')
user_repo = UserRepository('test.db')


@app.post('/users/new_user')
def add_user(user: AddUserModel) -> dict:
    user_repo.add(user)
    return {'message': f'user added'}

@app.get('/users/all_users')
def all_users():
    return user_repo.all_users()

@app.post('/users/{user_id}/dell_user')
def dell_user(user_id: int) -> dict:
    user_repo.dell_user(user_id)
    return {'message': f'user deleted'}

@app.post('/tasks/new_task')
def add_task(new_task: AddTaskModel) -> dict:
    task_repo.add(new_task)
    return {'message': 'task added'}

@app.post('/tasks/{task_id}/finish_task')
def finish_task(task_id: int) -> dict:
    task_repo.finish_task(task_id)
    return {'message': f'task complete'}

@app.get("/tasks/all_tasks")
def all_tasks():
    return task_repo.all_tasks()

@app.get("/tasks/done_tasks")
def done_tasks():
    return task_repo.get_tasks_by_status(True)

@app.get("/tasks/not_done_tasks")
def not_done_tasks():
    return task_repo.get_tasks_by_status(False)

@app.get("/tasks/{user_id}/user_tasks")
def user_tasks(user_id: int):
    return task_repo.user_tasks(user_id)

@app.post('/tasks/change_task')
def change_task(new_task: ChangeTaskModel) -> dict:
    task_repo.change_task(new_task)
    return {'message': f'task changed'}

@app.post('/tasks/{task_id}/dell_task')
def dell_task(task_id: int) -> dict:
    task_repo.dell_task(task_id)
    return {'message': f'task deleted'}