import sqlite3
from models import AddUserModel, UserModel, AddTaskModel, TaskModel, UserTaskModel, ChangeTaskModel

class Repository:
    def __init__(self, db_path = 'test.db'):
        self.db_path = db_path


class UserRepository(Repository):
    def add(self, user: AddUserModel):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (user_name) VALUES (:user_name)', {"user_name": user.user_name})
            conn.commit()

    def all_users(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            db_users = cursor.fetchall()
            return [UserModel(user_id=user[0], user_name=user[1]) for user in db_users]

    def dell_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE user_id = :user_id', {'user_id': user_id})
            conn.commit()


class TaskRepository(Repository):
    def add(self, n_task: AddTaskModel):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (task, user_id) VALUES (:task, :user_id)', {"task": n_task.task, "user_id": n_task.user_id})
            conn.commit()

    def finish_task(self, task_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET done = :done WHERE task_id = :task_id', {'done': True, "task_id": task_id})
            conn.commit()

    def all_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT t.task_id, t.task, t.done, u.user_id, u.user_name
                            FROM tasks AS t
                            INNER JOIN users AS u ON t.user_id = u.user_id''')
            task_list = cursor.fetchall()
            return [TaskModel(task_id = t[0], task = t[1], done = t[2], user_id = t[3]) for t in task_list]

    def get_tasks_by_status(self, status: bool):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT t.task_id, t.task, t.done, u.user_id, u.user_name
                            FROM tasks AS t
                            INNER JOIN users AS u ON t.user_id = u.user_id
                            WHERE t.done = :status''', {'status': status})
            task_list = cursor.fetchall()
            return [TaskModel(task_id=t[0], task=t[1], done=t[2], user_id=t[3]) for t in task_list]


    def user_tasks(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT t.task_id, t.task, t.done, u.user_id, u.user_name
                            FROM tasks AS t
                            INNER JOIN users AS u ON t.user_id = u.user_id
                            WHERE u.user_id = :user_id''', {'user_id': user_id })
            db_us_ts = cursor.fetchall()
            return [UserTaskModel(task_id=ut[0], task=ut[1], done=ut[2], user_id=ut[3], user_name=ut[4]) for ut in db_us_ts]

    def change_task(self, new_task: ChangeTaskModel):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET task = :new_task WHERE task_id = :task_id', {'task_id': new_task.task_id, 'new_task': new_task.new_task})
            conn.commit()

    def dell_task(self, task_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE task_id = :task_id', {'task_id': task_id})
            conn.commit()