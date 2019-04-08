# services/users/project/__init__.py

from flask import Flask, jsonify

# instanciado la app
app = Flask(__name__)

# configurar config
app.config.from_object('project.config.DevelopmentConfig')  # nuevo

@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
