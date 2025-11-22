from fastapi import FastAPI
from repository import UserRepository, TaskRepository
from models import AddUserModel, UserModel, AddTaskModel, TaskModel, UserTaskModel, ChangeTaskModel
from typing import List

app = FastAPI()

task_repo = TaskRepository('test.db')
user_repo = UserRepository('test.db')

def return_tm_list(task_list: list):
    return [TaskModel(task_id = t[0], task = t[1], done = t[2], user_id = t[3]) for t in task_list]


@app.post('/users/new_user')
def add_user(user: AddUserModel) -> dict:
    user_repo.add(user)
    return {'message': f'user added'}

@app.get('/users/all_users', response_model = List[UserModel])
def all_users():
    db_users = user_repo.all_users()
    return [UserModel(user_id = user[0], user_name = user[1]) for user in db_users]

@app.post('/users/{user_id}/dell_user')
def dell_user(user_id: int) -> dict:
    user_repo.dell_user(user_id)
    return {'message': f'user deleted'}

@app.post('/tasks/new_task')
def add_task(new_task: AddTaskModel):
    task_repo.add(new_task)
    return {'message': 'task added'}

@app.post('/tasks/{task_id}/finish_task')
def finish_task(task_id: int):
    task_repo.finish_task(task_id)
    return {'message': f'task complete'}

@app.get("/tasks/all_tasks")
def all_tasks():
    db_tasks = task_repo.all_tasks()
    return return_tm_list(db_tasks)

@app.get("/tasks/done_tasks")
def done_tasks():
    db_tasks = task_repo.get_tasks_by_status(True)
    return return_tm_list(db_tasks)

@app.get("/tasks/not_done_tasks")
def not_done_tasks():
    db_tasks = task_repo.get_tasks_by_status(False)
    return return_tm_list(db_tasks)

@app.get("/tasks{user_id}/user_tasks")
def user_tasks(user_id: int):
    db_us_ts = task_repo.user_tasks(user_id)
    return [UserTaskModel(task_id=ut[0], task=ut[1], done=ut[2], user_id=ut[3], user_name=ut[4]) for ut in db_us_ts]

@app.post('/tasks/change_task')
def change_task(new_task: ChangeTaskModel):
    task_repo.change_task(new_task)
    return {'message': f'task changed'}

@app.post('/tasks/{task_id}/dell_task')
def dell_task(task_id: int) -> dict:
    task_repo.dell_task(task_id)
    return {'message': f'task deleted'}