from pydantic import BaseModel

class AddUserModel(BaseModel):
    user_name: str

class UserModel(AddUserModel):
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