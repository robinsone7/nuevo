# services/users/project/tests/test_users.py

import json
import unittest

from project import db
from project.api.models import User

from project.tests.base import BaseTestCase

def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Tests para el servicio Users."""    
    
    def test_users(self):
        """Asegurando que la ruta /ping  se comporta correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Asegurando que un nuevo usuario pueda ser agregado a la base de datos."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'robinson',
                    'email': 'robinson.espinal@uperu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('robinson.espinal@uperu.edu.pe ha sido agregado', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Asegurando que se produzca un error si el objeto json esta vacio."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida', data['message'])
            self.assertIn('falló', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Asegurando que se produzca un error si el objeto json no tiene una clave"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'robinson.espinal@uperu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida', data['message'])
            self.assertIn('falló', data['status'])

    def test_add_user_duplicate_email(self):
        """Asegurando que se produzca un error si el email ya existe"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'robinson',
                    'email': 'robinson.espinal@uperu.edu.pe'
                }),
                content_type='application/json',
            )
            response=self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'robinson',
                    'email': 'robinson.espinal@uperu.edu.pe'
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento. EL email ya exite', data['message'])
            self.assertIn('falló', data['status'])

    def test_single_user(self):
        """ Asegurando de que el usuario individual se comporte correctamente."""
        user = add_user('robinson', 'robinson.espinal@uperu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('robinson', data['data']['username'])
            self.assertIn('robinson.espinal@uperu.edu.pe', data['data']['email'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_user_no_id(self):
        """Asegúrese de que se arroje un error si no se proporciona una identificación."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])
 
    def test_single_user_incorrect_id(self):
        """Asegurando de que se arroje un error si la identificación no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])      

    def test_all_users(self):
        """ Asegurando de que todos los usuarios se comporten correctamente."""
        add_user('robinson', 'robinson.espinal@uperu.edu.pe')
        add_user('fredy', 'abelthf@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('robinson', data['data']['users'][0]['username'])
            self.assertIn('robinson.espinal@uperu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('fredy', data['data']['users'][1]['username'])
            self.assertIn('abelthf@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('satisfactorio', data['estado'])


if __name__ == '__main__':
    unittest.main()

