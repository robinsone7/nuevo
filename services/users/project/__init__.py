# services/users/project/__init__.py


import os  # nuevo
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # nuevo


# instanciando la db
db = SQLAlchemy()  # nuev

def create_app(script_info=None):
    #Intanciar la app
    app = Flask(__name__)
    # establecer configuracion
    app_settings = os.getenv('APP_SETTINGS')   # Nuevo
    app.config.from_object(app_settings)       # Nuevo
    #configurar las extensiones
    db.init_app(app)

    #registrar blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    #shell context para flax cli
    @app.shell_context_processor
    def ctx():
        return {'app':app,'db':db}
    return app

