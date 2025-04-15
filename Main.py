from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from Modules import *


app = Flask(__name__, template_folder='templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase/API_DB.db'
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/h/<name>')
def hello(name):
    return render_template('index.html', name=name)

@app.route('/MySite/API/', methods=['GET', 'POST'])
def getDb():
   username = request.form['name']
   password = request.form['password']
   email = request.form['email']
   new_user = User(username=username, email=email, password=password)
   db.session.add(new_user)
   db.session.commit()
   return jsonify({'UserCreationStatus': db.session.connection,
                   'CreatedUser': new_user.__repr__})

if __name__ == '__main__':
  app.run(debug=True)