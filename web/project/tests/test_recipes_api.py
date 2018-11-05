# project/test_recipes_api.py


import os
import unittest
from flask import json
from base64 import b64encode
from werkzeug.datastructures import FileStorage

from project import app, db, mail
from project.models import Recipe, User


TEST_DB = 'test.db'


class RecipesApiTests(unittest.TestCase):
    admin_email = 'kennedyfamilyrecipes@gmail.com'
    admin_password = 'FlaskIsAwesome'
    user_email = 'patkennedy79@gmail.com'
    user_password = 'FlaskRules'

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.create_users()
        self.create_recipes()
        mail.init_app(app)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


    ########################
    #### helper methods ####
    ########################

    def create_users(self):
        # Create a new user with admin role for testing
        new_user = User(self.admin_email, self.admin_password, role='admin')
        db.session.add(new_user)
        db.session.commit()

        # Create a new user with standard permissions
        new_user2 = User(self.user_email, self.user_password)
        db.session.add(new_user2)
        db.session.commit()
        return

    def create_recipes(self):
        user1 = User.query.filter_by(email=self.admin_email).first()
        recipe1 = Recipe('Hamburgers', 'Classic dish elevated with pretzel buns.', user1.id, True)
        recipe2 = Recipe('Mediterranean Chicken', 'Grilled chicken served with pitas, hummus, and sauted vegetables.', user1.id, True)
        recipe3 = Recipe('Tacos', 'Ground beef tacos with grilled peppers.', user1.id, False)
        recipe4 = Recipe('Homemade Pizza', 'Homemade pizza made using pizza oven', user1.id, False)
        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.add(recipe3)
        db.session.add(recipe4)
        db.session.commit()

    def authenticate_user(self, email, password):
        auth = 'Basic ' + b64encode((email + ':' + password).encode('utf-8')).decode('utf-8')
        headers = {}
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        return self.app.get('/get-auth-token', headers=headers)

    def get_headers_authenticated_admin(self):
        headers = {}
        response = self.authenticate_user(self.admin_email, self.admin_password)
        json_data = json.loads(response.data.decode('utf-8'))
        auth = 'Basic ' + b64encode((json_data['token'] + ':' + 'unused').encode('utf-8')).decode('utf-8')
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        return headers

    ###############
    #### tests ####
    ###############

    def test_recipes_api_valid_authentication(self):
        response = self.authenticate_user(self.admin_email, self.admin_password)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.data)
        self.assertIn('private', response.headers['Cache-Control'])
        self.assertIn('no-cache', response.headers['Cache-Control'])
        self.assertIn('no-store', response.headers['Cache-Control'])
        self.assertIn('max-age=0', response.headers['Cache-Control'])

    def test_recipes_api_invalid_authentication_normal_user(self):
        response = self.authenticate_user(self.user_email, self.user_password)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized', json_data['error'])
        self.assertIn('please authenticate', json_data['message'])

    def test_recipes_api_invalid_authentication_invalid_user(self):
        response = self.authenticate_user(self.admin_email, 'FlaskIsOK')
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized', json_data['error'])
        self.assertIn('please authenticate', json_data['message'])

    def test_recipes_api_invalid_token(self):
        headers = {}
        response = self.authenticate_user(self.admin_email, self.admin_password)
        json_data = json.loads(response.data.decode('utf-8'))
        token = 'InvalidTokenInvalidToken'
        auth = 'Basic ' + b64encode((token + ':' + 'unused').encode('utf-8')).decode('utf-8')
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        response = self.app.get('/api/v1_2/recipes', headers=headers)

        self.assertEqual(response.status_code, 401)

    def test_recipes_api_get_all_recipes(self):
        headers = self.get_headers_authenticated_admin()
        response = self.app.get('/api/v1_2/recipes', headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_recipes_api_create_new_recipe(self):
        headers = self.get_headers_authenticated_admin()
        json_data = {'title': 'Tacos2', 'description': 'My favorite tacos!', 'recipe_type': 'Dinner'}
        response = self.app.post('/api/v1_2/recipes', data=json.dumps(json_data), headers=headers, follow_redirects=True)

        self.assertEqual(response.status_code, 201)
        self.assertIn('/api/v1_2/recipes/5', response.headers['Location'])

    def test_recipes_api_get_individual_recipe_valid(self):
        headers = self.get_headers_authenticated_admin()
        response = self.app.get('/api/v1_2/recipes/1', headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Hamburgers', json_data['title'])
        self.assertIn('Classic dish elevated with pretzel buns.', json_data['description'])
        self.assertIn('api/v1_2/recipes/1', json_data['self_url'])

    def test_recipes_api_get_individual_recipe_invalid(self):
        headers = self.get_headers_authenticated_admin()
        response = self.app.get('/api/v1_2/recipes/5', headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('invalid resource URI', json_data['message'])
        self.assertIn('not found (API!)', json_data['error'])

    def test_recipes_api_delete_recipe_valid(self):
        headers = self.get_headers_authenticated_admin()
        response = self.app.delete('/api/v1_2/recipes/2', headers=headers, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_recipes_api_delete_recipe_invalid(self):
        headers = self.get_headers_authenticated_admin()
        response = self.app.delete('/api/v1_2/recipes/16', headers=headers, follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('invalid resource URI', json_data['message'])
        self.assertIn('not found (API!)', json_data['error'])

    def test_recipes_api_put_recipe_valid(self):
        headers = self.get_headers_authenticated_admin()
        json_data = {'title': 'Updated recipe', 'description': 'My favorite recipe'}
        response = self.app.put('/api/v1_2/recipes/3', data=json.dumps(json_data), headers=headers, follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('True', json_data['result'])

    def test_recipes_api_put_recipe_invalid(self):
        headers = self.get_headers_authenticated_admin()
        json_data_input = {'title': 'Updated recipe', 'description': 'My favorite recipe'}
        response = self.app.put('/api/v1_2/recipes/15', data=json.dumps(json_data_input), headers=headers, follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('invalid resource URI', json_data['message'])
        self.assertIn('not found (API!)', json_data['error'])

    def test_recipes_api_check_etag(self):
        headers = self.get_headers_authenticated_admin()
        response = self.app.get('/api/v1_2/recipes', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.headers['ETag'])
        etag = response.headers['ETag']
        headers['If-None-Match'] = etag
        response2 = self.app.get('/api/v1_2/recipes', headers=headers)

        self.assertEqual(response2.status_code, 304)

        headers['If-None-Match'] = 'asfjskdjflakdsjflsdkfjsdlkfj'  # INVALID
        response3 = self.app.get('/api/v1_2/recipes', headers=headers)

        self.assertEqual(response3.status_code, 200)

    def test_recipes_api_sending_file(self):
        headers = self.get_headers_authenticated_admin()
        with open(os.path.join('project', 'tests', 'IMG_6127.JPG'), 'rb') as fp:
            file = FileStorage(fp)
            response = self.app.put('/api/v1_2/recipes/2', data={'recipe_image': file}, headers=headers,
                                    content_type='multipart/form-data', follow_redirects=True)
            json_data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertIn('True', json_data['result'])


if __name__ == "__main__":
    unittest.main()
