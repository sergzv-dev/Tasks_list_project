from fastapi import FastAPI, Depends
from repository import UserRepository, TaskRepository, AuthorizRepository
from models import NameUserModel, AddTaskModel, ChangeTaskModel, AuthorizUser, AuthorizUserHash
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from token_manager import verify_token
from pass_hash_manager import hash_password, verify_password
from token_manager import create_token

app = FastAPI()
auth_scheme = HTTPBearer()

task_repo = TaskRepository('test.db')
user_repo = UserRepository('test.db')

def chek_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    payload = verify_token(token)
    return payload


@app.post('/signup')
def signup(new_user: AuthorizUser):
    hash_pass = hash_password(new_user.password)
    authoriz_repo.add(AuthorizUserHash(nickname=new_user.name, hash_pass=hash_pass))
    return {'message': 'successful authorization'}

@app.post('/signin')
def signin(user: AuthorizUser):
    hash_pass = hash_password(user.password)
    bd_hash_pass = authoriz_repo.chek_pass(AuthorizUserHash(nickname=user.name, hash_pass=hash_pass))
    if not verify_password(user.password, bd_hash_pass):
        raise HTTPException(status_code=401, detail='wrong login or password')
    token = create_token(user.nickname)
    return {'access token': token}

@app.post('/users/new_user')
def add_user(user: NameUserModel, _: dict = Depends(chek_token)) -> dict:
    user_repo.add(user)
    return {'message': 'user added'}

@app.get('/users/all_users')
def all_users(_: dict = Depends(chek_token)):
    return user_repo.all_users()

@app.post('/users/{user_id}/dell_user')
def dell_user(user_id: int, _: dict = Depends(chek_token)) -> dict:
    user_repo.dell_user(user_id)
    return {'message': 'user deleted'}

@app.post('/tasks/new_task')
def add_task(new_task: AddTaskModel, _: dict = Depends(chek_token)) -> dict:
    task_repo.add(new_task)
    return {'message': 'task added'}

@app.post('/tasks/{task_id}/finish_task')
def finish_task(task_id: int, _: dict = Depends(chek_token)) -> dict:
    task_repo.finish_task(task_id)
    return {'message': 'task complete'}

@app.get('/tasks/all_tasks')
def all_tasks(_: dict = Depends(chek_token)):
    return task_repo.all_tasks()

@app.get('/tasks/done_tasks')
def done_tasks(_: dict = Depends(chek_token)):
    return task_repo.get_tasks_by_status(True)

@app.get('/tasks/not_done_tasks')
def not_done_tasks(_: dict = Depends(chek_token)):
    return task_repo.get_tasks_by_status(False)

@app.get('/tasks/{user_id}/user_tasks')
def user_tasks(user_id: int, _: dict = Depends(chek_token)):
    return task_repo.user_tasks(user_id)

@app.post('/tasks/change_task')
def change_task(new_task: ChangeTaskModel, _: dict = Depends(chek_token)) -> dict:
    task_repo.change_task(new_task)
    return {'message': 'task changed'}

@app.post('/tasks/{task_id}/dell_task')
def dell_task(task_id: int, _: dict = Depends(chek_token)) -> dict:
    task_repo.dell_task(task_id)
    return {'message': 'task deleted'}