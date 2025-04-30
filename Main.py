from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3 # подключаем Sqlite в наш проект 
import hashlib # библиотека для хеширования 

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

#  наша корневая страиницу лендинда 
@app.route('/')
def home():
  # Загрузка и отображение главной страницы (Authorization page)
  return redirect(url_for('admin_login'))

# страница формы логина в админ панель  
@app.route('/adm_login', methods=['GET', 'POST'])
def admin_login():
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
      # и делаем переадресацию пользователя на новую страницу -> в нашу адимнку
      return redirect(url_for('admin_panel'))

  else:
    error = 'Неправильное имя пользователя или пароль'

  return render_template('AuthorizationPage.html', error=error)

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
  
  conn = get_db_connection()
  blocks = conn.execute('SELECT * FROM users').fetchall()  # Получаем все записи из таблицы content
  conn.close()

  # Преобразование данных из БД в список словарей
  blocks_list = [dict(ix) for ix in blocks]
  # print(blocks_list) [{строка 1 из бд},{строка 2 из бд},{строка 3 из бд}, строка 4 из бд]

  # Теперь нужно сделать группировку списка в один словарь json
  # Группировка данных в словарь JSON
  json_data = {}
  for raw in blocks_list:
    # Создание новой записи, если ключ еще не существует
    if raw['group_id'] not in json_data:
      json_data[raw['group_id']] = []

    # Добавление данных в существующий ключ
    json_data[raw['group_id']].append({
            'id': raw['id'],
            'username': raw['username'],
            'third_name': raw['third_name'],
            'second_name': raw['second_name'],
            'first_name': raw['first_name'],
            'rights_id': raw['rights_id'],
            'group_id': raw['group_id'],
            'password': raw['password']
    })

    # print(json_data)
    # передаем на json на фронт - далее нужно смотреть admin_panel.html и обрабатывать там
  return render_template('AdminPanel.html', json_data=json_data)

if __name__ == '__main__':
  app.run(debug=True)