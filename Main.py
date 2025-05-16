from flask import Flask, render_template, redirect, url_for, request, session
import DB_Views
import sqlite3 # подключаем Sqlite в наш проект 
import hashlib # библиотека для хеширования 
import os
from werkzeug.utils import secure_filename

# Flask - библиотека для запуска нашего приложения Flask - app
# render_template - нужен для то чтобы ваша страница html отобразилась корреткно
# redirect - нам понадобится для обработки запросы формы где мы перенаприм пользователя на страницу админ панели
# url_for - вспомогательна библиотека для того чтобы сделать правильный переход по ссылке в нашем случеш мы будем ссылаться на adm_panel
# request - обработчик запросов GET/POST и дргуих 

app = Flask(__name__)
app.secret_key = 'Ca641Oc94Cb49aK67baS7e31U66fdCce76fKc693'  # подствавьте свой секретный ключ
# секретный ключ для хеширования данных сессии при авторизации

# Устанавливаем соединение с Базой Данных
def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn

@app.route('/getUser', methods=['GET'])
def getUser():
  print(request)
  username = request.form['username'] # обрабатываем запрос с нашей формы который имеет атрибут name="username"
  password = request.form['password'] # обрабатываем запрос с нашей формы который имеет атрибут name="password"
  hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() # шифруем пароль в sha-256

    # устанавливаем соединение с БД
  conn = get_db_connection() 
    # создаем запрос для поиска пользователя по username,
    # если такой пользователь существует, то получаем все данные id, password
  user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    # закрываем подключение БД
  conn.close() 
            
    # теперь проверяем если данные сходятся формы с данными БД
  if user and user['password'] == hashed_password:
      # в случае успеха создаем сессию в которую записываем id пользователя
    print("Hello, ", user['second_Name'], user['first_Name'])

    return f"Hello, {user['second_Name']} {user['first_Name']}"
  else:
    return "invalid username or password"

#  наша корневая страиницу лендинда 
@app.route('/')
def home():
  # Загрузка и отображение главной страницы (Authorization page)
  return redirect(url_for('admin_login'))

# страница формы логина в админ панель  
@app.route('/adm_login', methods=['GET', 'POST'])
def admin_login():

  if 'user_id' in session:
    return redirect(url_for('admin_panel'))

  error = None # обнуляем переменную ошибок 
  if request.method == 'POST':
    username = request.form['username'] # обрабатываем запрос с нашей формы который имеет атрибут name="username"
    password = request.form['password'] # обрабатываем запрос с нашей формы который имеет атрибут name="password"
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() # шифруем пароль в sha-256

    # устанавливаем соединение с БД
    conn = get_db_connection() 
    # создаем запрос для поиска пользователя по username,
    # если такой пользователь существует, то получаем все данные id, password
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    # закрываем подключение БД
    conn.close() 
            
    # теперь проверяем если данные сходятся формы с данными БД
    if user and user['password'] == hashed_password:
      # в случае успеха создаем сессию в которую записываем id пользователя
      session['user_id'] = user['id']
      session['second_Name'] = user['second_Name']
      session['first_Name'] = user['first_Name']
      # и делаем переадресацию пользователя на новую страницу -> в нашу адимнку
      return redirect(url_for('admin_panel'))

  else:
    error = 'Неправильное имя пользователя или пароль'

  return render_template('AuthorizationPage.html', error=error)


@app.route('/update_content', methods=['POST'])
def update_content():

    content_id = request.form['id']
    short_title = request.form['short_title']
    title = request.form['title']
    altimg = request.form['altimg']
    contenttext = request.form['contenttext']

    # Обработка загруженного файла
    # file = request.files['img']

    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     save_path = os.path.join(path_to_save_images, filename)
    #     imgpath = "/static/imgs/"+filename
    #     file.save(save_path)
        # Обновите путь изображения в вашей базе данных

    # Обновление данных в базе
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # if file:
    #     cursor.execute('UPDATE content SET short_title=?, img=?, altimg=?, title=?, contenttext=? WHERE id=?',
    #                (short_title, imgpath, altimg, title, contenttext, content_id))
    # else:
    #     cursor.execute('UPDATE content SET short_title=?, altimg=?, title=?, contenttext=? WHERE id=?',
    #                    (short_title, altimg, title, contenttext, content_id))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
  # Удаление данных пользователя из сессии
  session.clear()
  # Перенаправление на главную страницу или страницу входа
  return redirect(url_for('home'))

# страница админ панели
@app.route('/admin_panel')
def admin_panel():
  # делаем доп проверку если сессия авторизации была создана 
  if 'user_id' not in session:
    return redirect(url_for('admin_login'))
  
   # Получаем список всех таблиц
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
  table_names = [row[0] for row in cursor.fetchall()]

  tables_data = {}
  for table in table_names:
    if 'sqlite_sequence' in table:
      continue
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in cursor.fetchall()]

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    Rows_List = [dict(ix) for ix in rows]

    json_data = {}
    for raw in Rows_List:
      if raw[columns[1]] not in json_data:
        json_data[raw[columns[1]]] = []

      
      json_data[raw[columns[1]]].append({ columnName: raw[columnName] for columnName in columns
    #           'id': raw['id'],
    #           'username': raw['username'],
    #           'third_Name': raw['third_Name'],
    #           'second_Name': raw['second_Name'],
    #           'first_Name': raw['first_Name'],
    #           'rights_id': raw['rights_id'],
    #           'group_id': raw['group_id'],
    #           'password': raw['password']
      })

    
    tables_data[DB_Views.getView(table)] = {'data': json_data, 'columns': columns}
    
  conn.close()

  # conn = get_db_connection()
  # blocks = conn.execute('SELECT * FROM users').fetchall()  # Получаем все записи из таблицы content
  # conn.close()

  # # Преобразование данных из БД в список словарей
  # blocks_list = [dict(ix) for ix in blocks]
  # # print(blocks_list) [{строка 1 из бд},{строка 2 из бд},{строка 3 из бд}, строка 4 из бд]

  # # Теперь нужно сделать группировку списка в один словарь json
  # # Группировка данных в словарь JSON
  # json_data = {}
  # for raw in blocks_list:
  #   # Создание новой записи, если ключ еще не существует
  #   if raw['group_id'] not in json_data:
  #     json_data[raw['group_id']] = []

  #   # Добавление данных в существующий ключ
  #   json_data[raw['group_id']].append({
  #           'id': raw['id'],
  #           'username': raw['username'],
  #           'third_Name': raw['third_Name'],
  #           'second_Name': raw['second_Name'],
  #           'first_Name': raw['first_Name'],
  #           'rights_id': raw['rights_id'],
  #           'group_id': raw['group_id'],
  #           'password': raw['password']
  #   })

    # print(json_data)
    # передаем на json на фронт - далее нужно смотреть admin_panel.html и обрабатывать там
  return render_template('AdminPanel.html', json_data=tables_data, username=session['first_Name'])

if __name__ == '__main__':
  app.run(debug=True)