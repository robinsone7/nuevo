# services/users/project/__init__.py


import os  # nuevo
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy  # nuevo


# instanciado la app
app = Flask(__name__)

# establecer configuraicon
app_settings = os.getenv('APP_SETTINGS')   # Nuevo
app.config.from_object(app_settings)       # Nuevo

# instanciando la db
db = SQLAlchemy(app)  # nuevo


# modelo
class User(db.Model):  # nuevo
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


# rutas
@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
