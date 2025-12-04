import sqlite3
from models import DBAuthUser, DBUser, DBTask, DBPagination

class Repository:
    def __init__(self, db_path = 'test.db'):
        self.db_path = db_path


class UserRepository(Repository):
    def new_user(self, user: DBAuthUser):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (user_name, hash_pass) VALUES (:user_name, :hash_pass)',
                           {'user_name': user.user_name, 'hash_pass': user.hash_pass})
            conn.commit()

    def user_hash(self, user: DBAuthUser):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT user_id, role, user_name, hash_pass FROM users
                                WHERE user_name = :user_name''',
                           {'user_name': user.user_name})
            row = cursor.fetchone()
        return DBAuthUser(user_id = row[0], role= row[1], user_name = row[2], hash_pass =  row[3]) if row else DBAuthUser()


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
            rows = cursor.fetchall()
        return [DBTask(task_id=row[0], task=row[1], done=row[2]) for row in rows]

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
            rows = cursor.fetchall()
        return [DBTask(task_id=row[0], task=row[1], done=row[2]) for row in rows]

    def change_task(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET task = :new_task WHERE task_id = :task_id AND user_id = :user_id',
                           {'new_task': task.task, 'task_id': task.task_id, 'user_id': task.user_id})
            conn.commit()

    def dell_task(self, task: DBTask):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE task_id = :task_id AND user_id = :user_id',
                           {'task_id': task.task_id, 'user_id': task.user_id})
            conn.commit()

    def get_tasks_by_page (self, page: DBPagination):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT task_id, task, done FROM tasks
                            WHERE user_id = ? ORDER BY task_id LIMIT ? OFFSET ?'''
                           ,(page.user_id, page.limit, page.offset))
            rows = cursor.fetchall()
            tasks_list = [DBTask(task_id=row[0], task=row[1], done=row[2]) for row in rows]
            cursor.execute('SELECT COUNT(*) FROM tasks WERE WHERE user_id = ?', (page.user_id,))
            total = cursor.fetchone()[0]
        return DBPagination(limit = page.limit, offset = page.offset, total = total, data = tasks_list)

    def get_tasks_by_cur(self, page: DBPagination):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT task_id, task, done FROM tasks
                            WHERE user_id = ? AND task_id > ?
                            ORDER BY task_id LIMIT ?'''
                           ,(page.user_id, page.cur, page.limit + 1))
            rows = cursor.fetchall()
            check_tasks_list = [DBTask(task_id=row[0], task=row[1], done=row[2]) for row in rows]
            cursor.execute('SELECT COUNT(*) FROM tasks WERE WHERE user_id = ?', (page.user_id,))
            total = cursor.fetchone()[0]
        return DBPagination( total = total, data = check_tasks_list)


class AdminRepository(Repository):
    def new_admin(self, user: DBAuthUser):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (role, user_name, hash_pass) VALUES (:role, :user_name, :hash_pass)',
                           {'role': user.role, 'user_name': user.user_name, 'hash_pass': user.hash_pass})
            conn.commit()

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