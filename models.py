from pydantic import BaseModel

class AuthUser(BaseModel):
    user_name: str
    password: str

class TokenUser(BaseModel):
    user_id: int
    role: str
    user_name: str

class NewTaskModel(BaseModel):
    task: str

class ChangeTaskModel(BaseModel):
    task_id: int
    task: str

# Database models
class DBAuthUser(BaseModel):
    user_id: int | None = None
    role: str | None = None
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

class DBPagination(BaseModel):
    limit: int | None = None
    offset: int | None = None
    total: int | None = None
    cur: int | None = None
    next_cur: int | None = None
    has_more: bool | None = None
    user_id: int | None = None
    data: list | None = None