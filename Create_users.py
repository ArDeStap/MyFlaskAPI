import sqlite3
import hashlib

def create_userRights(description):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Добавление нового пользователя
    c.execute('INSERT INTO user_rights (description) VALUES (?)', [description])

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()   

def create_usersGroup(groupName):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Добавление нового пользователя
    c.execute('INSERT INTO groups (group_name) VALUES (?)', [groupName])

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()   

def create_user(kwargs):
    
    userData = kwargs
    
    # Хеширование пароля
    hashed_password = hashlib.sha256(kwargs['password'].encode('utf-8')).hexdigest()

    # Подключение к нашей базе данных
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Добавление нового пользователя
    c.execute('INSERT INTO users (username, password, third_name, second_name, first_name, rights_id, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)', 
              [kwargs['username'], hashed_password, kwargs['third_name'], kwargs['second_name'], kwargs['first_name'], kwargs['rights_id'], kwargs['group_id']])

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()


create_usersGroup('Administration Group')
create_userRights('Full Rights')

# Замените 'admin' и 'your_password' на желаемые имя пользователя и пароль
create_user({'username': 'admin', 'password': '123456789', 'third_name': 'Sergeyevich', 'second_name': 'Yukachev', 'first_name': 'Anton', 'rights_id': 1, 'group_id': 1})