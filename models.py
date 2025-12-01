from pydantic import BaseModel

class AuthUser(BaseModel):
    user_name: str
    password: str

#########

class NameUserModel(BaseModel):
    user_name: str

class UserModel(NameUserModel):
    user_id: int

class AddTaskModel(BaseModel):
    task: str
    user_id: int

class TaskModel(BaseModel):
    task_id: int
    task: str
    done: bool
    user_id: int

class UserTaskModel(BaseModel):
    task_id: int
    task: str
    done:bool
    user_id:int
    user_name: str

class ChangeTaskModel(BaseModel):
    task_id: int
    new_task: str

class AuthorizUser(BaseModel):
    nickname: str
    password: str

class AuthorizUserHash(BaseModel):
    nickname: str
    hash_pass: str

# Database models
class DBAuthUser(BaseModel):
    user_id: int | None = None
    user_name: str | None = None
    hash_pass: str | None = None


class DBUser(BaseModel):
    user_id: int | None = None
    user_name: str | None = None


class DBTask(BaseModel):
    task_id: int | None = None
    task: str | None = None
    done: bool | None = None
    user_id: int | None = None