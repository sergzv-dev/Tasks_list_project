from fastapi import FastAPI, Depends, HTTPException, Path, Query
from repository import UserRepository, TaskRepository, AdminRepository
from models import AuthUser, DBAuthUser, DBTask, TokenUser, NewTaskModel, ChangeTaskModel, DBPagination
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from token_manager import verify_token
from pass_hash_manager import hash_password, verify_password
from token_manager import create_token

app = FastAPI()
auth_scheme = HTTPBearer()

admin_repo = AdminRepository('test.db')
task_repo = TaskRepository('test.db')
user_repo = UserRepository('test.db')


def check_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    verified_user = verify_token(token)
    return verified_user

def admin_check_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    verified_user = verify_token(token)
    if verified_user.role != "admin":
        raise HTTPException(403, "Admins only")
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
def add_task(task: NewTaskModel, user: dict = Depends(check_token)) -> dict:
    task_repo.add(DBTask(task = task.task, user_id = user.user_id))
    return {'message': 'task added'}

@app.get('/tasks/all_tasks')
def all_my_tasks(user: dict = Depends(check_token)):
    return task_repo.all_user_tasks(DBTask(user_id = user.user_id))

@app.post('/tasks/finish_task/{task_id}')
def finish_task(task_id: int = Path(...), user: dict = Depends(check_token)) -> dict:
    task_repo.finish_task(DBTask(task_id = task_id, user_id = user.user_id))
    return {'message': 'task complete'}

@app.get('/tasks/done_tasks')
def done_tasks(user: dict = Depends(check_token)):
    return task_repo.get_tasks_by_status(DBTask(done = True, user_id = user.user_id))

@app.get('/tasks/not_done_tasks')
def not_done_tasks(user: dict = Depends(check_token)):
    return task_repo.get_tasks_by_status(DBTask(done = False, user_id = user.user_id))

@app.post('/tasks/change_task')
def change_task(task: ChangeTaskModel, user: dict = Depends(check_token)) -> dict:
    task_repo.change_task(DBTask(task_id = task.task_id, task = task.task, user_id = user.user_id))
    return {'message': 'task changed'}

@app.post('/tasks/dell_task/{task_id}')
def dell_task(task_id: int = Path(...), user: dict = Depends(check_token)) -> dict:
    task_repo.dell_task(DBTask(task_id = task_id, user_id = user.user_id))
    return {'message': 'task deleted'}

@app.get('/tasks/page_tasks')
def page_tasks(limit: int = Query(default=10, ge=1, le=100),
               offset: int = Query(default=0, ge=0),
               user: dict = Depends(check_token)):
    return task_repo.get_tasks_by_page(DBPagination(limit = limit, offset = offset, user_id = user.user_id))

@app.get('/tasks/page_tasks_cur')
def page_tasks_cur(limit: int = Query(default=10, ge=1, le=100),
               cur: int = Query(default=0),
               user: dict = Depends(check_token)):
    db_data = task_repo.get_tasks_by_cur(DBPagination(limit = limit, cur = cur, user_id = user.user_id))
    check_tasks_list = db_data.data
    total = db_data.total
    if len(check_tasks_list) == limit + 1:
        *tasks_list, last_task = check_tasks_list
        next_cur = last_task.task_id
        has_more = True
    else:
        tasks_list = check_tasks_list
        next_cur = None
        has_more = False
    return DBPagination(limit = limit, next_cur = next_cur, total = total, has_more =has_more, data = tasks_list)

#Admin endpoints
@app.post('/admin/signup')
def signup(new_user: AuthUser):
    hash_pass = hash_password(new_user.password)
    admin_repo.new_admin(DBAuthUser(role = 'admin',user_name = new_user.user_name, hash_pass = hash_pass))
    return {'message': 'successful authorization'}

@app.get('/admin/all_users')
def admin_all_users(_: dict = Depends(admin_check_token)):
    return admin_repo.admin_all_users()

@app.get('/admin/all_tasks')
def admin_all_tasks(_: dict = Depends(admin_check_token)):
    return admin_repo.admin_all_tasks()

@app.get('/admin/user_tasks')
def admin_users_tasks(_: dict = Depends(admin_check_token)):
    return admin_repo.admin_users_tasks()

@app.post('/admin/dell_user/{user_id}')
def admin_dell_user(user_id: int = Path(...), _: dict = Depends(admin_check_token)) -> dict:
    admin_repo.admin_dell_user(user_id)
    return {'message': 'user deleted'}
