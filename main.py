from fastapi import FastAPI, Depends, HTTPException
from repository import UserRepository, TaskRepository, AdminRepository
from models import AuthUser, DBAuthUser, DBTask, TokenUser, NewTaskModel, ChangeTaskModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from token_manager import verify_token
from pass_hash_manager import hash_password, verify_password
from token_manager import create_token

app = FastAPI()
auth_scheme = HTTPBearer()

admin_repo = AdminRepository('test.db')
task_repo = TaskRepository('test.db')
user_repo = UserRepository('test.db')

def chek_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    verified_user = verify_token(token)
    return verified_user


#Authorization
@app.post('/signup')
def signup(new_user: AuthUser):
    hash_pass = hash_password(new_user.password)
    user_repo.new_user(DBAuthUser(user_name = new_user.user_name, hash_pass = hash_pass))
    return {'message': 'successful authorization'}

@app.post('/signin')
def signin(user: AuthUser):
    db_user = user_repo.user_hash(DBAuthUser(user_name = user.user_name))
    if not verify_password(user.password, db_user.hash_pass):
        raise HTTPException(status_code=401, detail='wrong login or password')
    token = create_token(TokenUser(**db_user.model_dump()))
    return {'access token': token}


#User endpoints
@app.post('/tasks/new_task')
def add_task(task: NewTaskModel, user: dict = Depends(chek_token)) -> dict:
    task_repo.add(DBTask(task = task.task, user_id = user.user_id))
    return {'message': 'task added'}

@app.get('/tasks/all_tasks')
def all_my_tasks(user: dict = Depends(chek_token)):
    return task_repo.all_user_tasks(DBTask(user_id = user.user_id))

@app.post('/tasks/{task_id}/finish_task')
def finish_task(task_id: int, user: dict = Depends(chek_token)) -> dict:
    task_repo.finish_task(DBTask(task_id = task_id, user_id = user.user_id))
    return {'message': 'task complete'}

@app.get('/tasks/done_tasks')
def done_tasks(user: dict = Depends(chek_token)):
    return task_repo.get_tasks_by_status(DBTask(done = True, user_id = user.user_id))

@app.get('/tasks/not_done_tasks')
def not_done_tasks(user: dict = Depends(chek_token)):
    return task_repo.get_tasks_by_status(DBTask(done = False, user_id = user.user_id))

@app.post('/tasks/change_task')
def change_task(task: ChangeTaskModel, user: dict = Depends(chek_token)) -> dict:
    task_repo.change_task(DBTask(task_id = task.task_id, task = task.task, user_id = user.user_id))
    return {'message': 'task changed'}

@app.post('/tasks/{task_id}/dell_task')
def dell_task(task_id: int, user: dict = Depends(chek_token)) -> dict:
    task_repo.dell_task(DBTask(task_id = task_id, user_id = user.user_id))
    return {'message': 'task deleted'}


# #Admin endpoints
# @app.get('/users/all_users')
# def all_users(_: dict = Depends(chek_token)):
#     return user_repo.all_users()
#
# @app.post('/users/{user_id}/dell_user')
# def dell_user(user_id: int, _: dict = Depends(chek_token)) -> dict:
#     user_repo.dell_user(user_id)
#     return {'message': 'user deleted'}
#
# @app.get('/tasks/{user_id}/user_tasks')
# def user_tasks(user_id: int, _: dict = Depends(chek_token)):
#     return task_repo.user_tasks(user_id)
