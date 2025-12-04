import sqlite3

def fill_table():
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        for task_num in range(50):
            task = 'task number ' + str(task_num)
            user_id = 1
            cursor.execute('INSERT INTO tasks (task, user_id) VALUES (:task, :user_id)',
                           {'task': task, 'user_id': user_id})
        conn.commit()

fill_table()