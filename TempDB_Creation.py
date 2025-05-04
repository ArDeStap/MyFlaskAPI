import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('database.db')

# Создание курсора
c = conn.cursor()

# Создание таблицы Groups
c.execute('''CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL);''')

# Создание таблицы прав пользователей
c.execute('''CREATE TABLE IF NOT EXISTS user_rights (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          description TEXT);''')

# Создание таблицы Users
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER DEFAULT 1 PRIMARY KEY AUTOINCREMENT NOT NULL,
             username TEXT NOT NULL,
             password TEXT NOT NULL,
             third_Name TEXT,
             second_Name TEXT NOT NULL,
             first_Name TEXT NOT NULL,
             rights_id INTEGER,
             group_id INTEGER,
             FOREIGN KEY (rights_id) REFERENCES user_rights (id) ON DELETE SET NULL,
             FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE SET NULL);''')

# Создание таблицы созданных пользователем тестов
c.execute('''CREATE TABLE IF NOT EXISTS tests (
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          test_name TEXT NOT NULL,
          test_description TEXT,
          test_length INTEGER DEFAULT 0,
          creation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          last_update DATETIME DEFAULT CURRENT_TIMESTAMP,
          test_file BLOB,  
          creator_id INTEGER,
          FOREIGN KEY (creator_id) REFERENCES users (id) ON DELETE SET DEFAULT );''')

# Создание таблицы созданных пользователем структур компетенций 
c.execute('''CREATE TABLE IF NOT EXISTS structure_compitations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          struc_name TEXT NOT NULL,
          struc_description TEXT,
          structure_file BLOB,
          creator_id INTEGER,
          FOREIGN KEY (creator_id) REFERENCES users (id) ON DELETE SET DEFAULT );''')

# Создание таблицы созданных пользователем компетенций 
c.execute('''CREATE TABLE IF NOT EXISTS compitations(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          compitation_name TEXT NOT NULL,
          compitation_description TEXT,
          complition_percent REAL,
          structure_id INTEGER,
          FOREIGN KEY (structure_id) REFERENCES structure_compitations (id) ON DELETE SET DEFAULT );''')

# Создание таблицы созданных пользователем постов 
c.execute('''CREATE TABLE IF NOT EXISTS user_posts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          post_name TEXT,
          post_description TEXT,
          post_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
          creator_id INTEGER,
          FOREIGN KEY (creator_id) REFERENCES users (id) ON DELETE SET DEFAULT );''')


# Закрытие соединения с базой данных
conn.close()