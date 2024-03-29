# services/users/manage.py

import unittest


from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='robinson', email='robinson.espinal.uperu.edu.pe'))
    db.session.add(User(username='fredy', email='abelthf@gmail.com'))
    db.session.commit()

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Ejecutar los tests sin cobertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
    
if __name__ == '__main__':
    cli()
