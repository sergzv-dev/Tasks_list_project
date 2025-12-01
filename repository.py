import sqlite3
from models import DBAuthUser, DBUser, DBTask

class Repository:
    def __init__(self, db_path = 'test.db'):
        self.db_path = db_path


class UserRepository(Repository):
    def add(self, user: DBAuthUser):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (user_name, hash_pass) VALUES (:user_name, :hash_pass)',
                           {'user_name': user.user_name, 'hash_pass': user.hash_pass})
            conn.commit()

    def user_hash(self, user: DBAuthUser):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT user_id, user_name, hash_pass FROM users
                                WHERE user_name = :user_name AND hash_pass = :hash_pass''',
                           {'user_name': user.user_name, 'hash_pass': user.hash_pass})
            row = cursor.fetchone()
        return DBAuthUser(user_id = row[0], user_name = row[1], hash_pass =  row[2]) if row else None


class TaskRepository(Repository):
    def add(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (task, user_id) VALUES (:task, :user_id)',
                           {'task': task.task, 'user_id': task.user_id})
            conn.commit()

    def all_user_tasks(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT task_id, task, done FROM tasks WHERE user_id = :user_id',
                           {'user_id': task.user_id})
            task_list = cursor.fetchall()
            return [DBTask(task_id=t[0], task=t[1], done=t[2]) for t in task_list]

    def finish_task(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET done = :done WHERE task_id = :task_id AND user_id = :user_id',
                           {'done': True, "task_id": task.task_id, 'user_id': task.user_id})
            conn.commit()

    def get_tasks_by_status(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT task_id, task, done FROM tasks WHERE done = :done AND user_id = :user_id',
                           {'done': task.done, 'user_id': task.user_id})
            task_list = cursor.fetchall()
            return [DBTask(task_id=t[0], task=t[1], done=t[2]) for t in task_list]

    def change_task(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET task = :new_task WHERE task_id = :task_id AND user_id = :user_id',
                           {'new_task': task.new_task, 'task_id': task.task_id, 'user_id': task.user_id})
            conn.commit()

    def dell_task(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE task_id = :task_id AND user_id = :user_id',
                           {'task_id': task.task_id, 'user_id': task.user_id})
            conn.commit()


class AdminRepository(Repository):
    def admin_add(self, admin: DBAuthUser):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO admins (admin_name, hash_pass) VALUES (:admin_name, :hash_pass)',
                           {'admin_name': 'admin.' + admin.user_name, 'hash_pass': admin.hash_pass})

    def admin_hash(self, admin: DBAuthUser):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT admin_id, admin_name, hash_pass FROM admins
                                WHERE admin_name = :admin_name AND hash_pass = :hash_pass''',
                           {'admin_name': admin.user_name, 'hash_pass': admin.hash_pass})
            row = cursor.fetchone()
        return DBAuthUser(user_id = row[0], user_name = row[1], hash_pass =  row[2]) if row else None

    def admin_all_users(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id, user_name FROM users')
            rows = cursor.fetchall()
            return [DBUser(user_id=user[0], user_name=user[1]) for user in rows]

    def admin_all_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT task_id, task, done, user_id FROM tasks ORDER BY user_id, task_id')
            rows = cursor.fetchall()
            return [DBTask(task_id = row[0], task = row[1], done = row[2], user_id = row[3]) for row in rows]

    def admin_users_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT t.task_id, t.task, t.done, t.user_id, u.user_id, u.user_name
                            FROM tasks AS t
                            INNER JOIN users AS u ON t.user_id = u.user_id''')
            rows = cursor.fetchall()
            return [{'Task': DBTask(task_id = row[0], task = row[1], done = row[2], user_id = row[3]),
                     'User': DBUser(user_id = row[4], user_name = row[5])} for row in rows]

    def admin_dell_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE user_id = :user_id', {'user_id': user_id})
            conn.commit()