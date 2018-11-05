# project/test_recipes.py


import os
import unittest
from io import BytesIO

from project import app, db, mail
from project.models import Recipe, User


TEST_DB = 'test.db'


class RecipesTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        mail.init_app(app)
        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


    ########################
    #### helper methods ####
    ########################

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')

    def register_user2(self):
        self.app.get('/register', follow_redirects=True)
        self.register('stockwatchlistapp@gmail.com', 'FlaskIsGreat', 'FlaskIsGreat')

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')

    def login_user2(self):
        self.app.get('/login', follow_redirects=True)
        self.login('stockwatchlistapp@gmail.com', 'FlaskIsGreat')

    def logout_user(self):
        self.app.get('/logout', follow_redirects=True)

    def add_recipes(self):
        self.register_user()
        self.register_user2()
        user1 = User.query.filter_by(email='patkennedy79@gmail.com').first()
        user2 = User.query.filter_by(email='stockwatchlistapp@gmail.com').first()
        recipe1 = Recipe('Hamburgers', 'Classic dish elevated with pretzel buns.', user1.id, True)
        recipe2 = Recipe('Mediterranean Chicken', 'Grilled chicken served with pitas, hummus, and sauted vegetables.', user1.id, True)
        recipe3 = Recipe('Tacos', 'Ground beef tacos with grilled peppers.', user1.id, False)
        recipe4 = Recipe('Homemade Pizza', 'Homemade pizza made using pizza oven', user1.id, False)
        recipe5 = Recipe('Chicken Nuggets', 'Classic dish served with honey mustard', user2.id, True)
        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.add(recipe3)
        db.session.add(recipe4)
        db.session.add(recipe5)
        db.session.commit()


    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        # self.register_user()
        self.add_recipes()
        self.logout_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Kennedy Family Recipes', response.data)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Our Favorite Dairy-free and Soy-free Recipes!', response.data)
        self.assertNotIn(b'Hamburgers', response.data)
        self.assertNotIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertNotIn(b'Chicken Nuggets', response.data)

    def test_add_recipe_page(self):
        self.register_user()
        response = self.app.get('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a New Recipe', response.data)

    def test_add_recipe(self):
        self.register_user()
        app_client = app.test_client()
        app_client.post('/register',
                        data=dict(email='patkennedy79@gmail.com', password='FlaskIsAwesome', confirm='FlaskIsAwesome'),
                        follow_redirects=True)
        app_client.post('/login',
                        data=dict(email='patkennedy79@gmail.com', password='FlaskIsAwesome'),
                        follow_redirects=True)
        response = app_client.post('/add',
                                   buffered=True,
                                   content_type='multipart/form-data',
                                   data={'recipe_title': 'Hamburgers2',
                                         'recipe_description': 'Delicious hamburger with pretzel rolls',
                                         'recipe_type': 'Dinner',
                                         'recipe_steps': 'Step 1 Step 2 Step 3',
                                         'recipe_ingredients': 'Ingredient #1 Ingredient #2',
                                         'recipe_inspiration': 'http://www.foodnetwork.com/blaa',
                                         'recipe_image': (BytesIO(b'my file contents'), 'image001.jpg')},
                                   follow_redirects=True)
        self.assertIn(b'New recipe, Hamburgers2, added!', response.data)

    def test_add_invalid_recipe(self):
        self.register_user()
        response = self.app.post(
            '/add',
            data=dict(recipe_title='',
                      recipe_description='Delicious hamburger with pretzel rolls'),
            follow_redirects=True)
        self.assertIn(b'ERROR! Recipe was not added.', response.data)
        self.assertIn(b'This field is required.', response.data)

    def test_recipe_detail_public_recipe(self):
        # self.register_user()
        self.add_recipes()
        self.logout_user()
        response = self.app.get('/recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Public', response.data)
        self.assertNotIn(b'patkennedy79@gmail.com', response.data)
        self.login_user()
        response = self.app.get('/recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Public', response.data)
        self.assertIn(b'patkennedy79@gmail.com', response.data)
        self.logout_user()
        self.login_user2()
        response = self.app.get('/recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Public', response.data)
        self.assertNotIn(b'patkennedy79@gmail.com', response.data)
        self.assertIn(b'stockwatchlistapp@gmail.com', response.data)
        self.logout_user()

    def test_recipe_detail_private_recipe(self):
        # self.register_user()
        self.add_recipes()
        self.login_user()
        response = self.app.get('/recipe/3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tacos', response.data)
        self.assertIn(b'Private', response.data)
        self.assertIn(b'patkennedy79@gmail.com', response.data)

    def test_recipe_detail_private_recipe_invalid_user(self):
        # self.register_user()
        self.add_recipes()
        self.login_user2()
        response = self.app.get('/recipe/3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error! Incorrect permissions to access this recipe.', response.data)

    def test_recipe_edit_valid_user(self):
        self.add_recipes()
        self.login_user()
        response = self.app.get('/edit/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertIn(b'Public', response.data)
        self.assertIn(b'patkennedy79@gmail.com', response.data)

    def test_recipe_edit_invalid_user(self):
        self.add_recipes()
        self.login_user2()
        response = self.app.get('/edit/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error! Incorrect permissions to edit this recipe.', response.data)

    def test_recipe_edit_invalid_recipe(self):
        self.add_recipes()
        response = self.app.get('/edit/17', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_recipe_delete_valid_user(self):
        self.add_recipes()
        self.login_user()
        response = self.app.get('/delete/4', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Homemade Pizza was deleted.', response.data)

    def test_recipe_delete_invalid_user(self):
        self.add_recipes()
        self.login_user2()
        response = self.app.get('/delete/4', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error! Incorrect permissions to delete this recipe.', response.data)

    def test_recipe_delete_invalid_recipe(self):
        self.add_recipes()
        response = self.app.get('/delete/234', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_recipe_all_recipes(self):
        self.add_recipes()
        response = self.app.get('/recipes/All', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertIn(b'Chicken Nuggets', response.data)
        self.login_user()
        response = self.app.get('/recipes/All', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertIn(b'Tacos', response.data)
        self.assertIn(b'Homemade Pizza', response.data)
        self.assertIn(b'Chicken Nuggets', response.data)
        self.logout_user()
        self.login_user2()
        response = self.app.get('/recipes/All', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertIn(b'Chicken Nuggets', response.data)
        self.logout_user()

    def test_recipe_types(self):
        self.add_recipes()
        response = self.app.get('/recipes/Breakfast', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No recipes have been created!', response.data)
        self.assertNotIn(b'Hamburgers', response.data)
        self.assertNotIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertNotIn(b'Chicken Nuggets', response.data)
        response = self.app.get('/recipes/Lunch', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No recipes have been created!', response.data)
        self.assertNotIn(b'Hamburgers', response.data)
        self.assertNotIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertNotIn(b'Chicken Nuggets', response.data)
        response = self.app.get('/recipes/Dessert', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No recipes have been created!', response.data)
        self.assertNotIn(b'Hamburgers', response.data)
        self.assertNotIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertNotIn(b'Chicken Nuggets', response.data)
        response = self.app.get('/recipes/Drink', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No recipes have been created!', response.data)
        self.assertNotIn(b'Hamburgers', response.data)
        self.assertNotIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertNotIn(b'Chicken Nuggets', response.data)
        response = self.app.get('/recipes/Drinks', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ERROR! Invalid recipe type selected.', response.data)
        self.assertNotIn(b'Hamburgers', response.data)
        self.assertNotIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertNotIn(b'Chicken Nuggets', response.data)
        response = self.app.get('/recipes/Side Dish', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No recipes have been created!', response.data)
        self.assertNotIn(b'Hamburgers', response.data)
        self.assertNotIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)
        self.assertNotIn(b'Chicken Nuggets', response.data)

    def test_edit_recipe_fields(self):
        self.add_recipes()
        app_client = app.test_client()
        app_client.post('/login',
                        data=dict(email='patkennedy79@gmail.com', password='FlaskIsAwesome'),
                        follow_redirects=True)
        response = app_client.get('/edit/3', follow_redirects=True)
        self.assertIn(b'Edit Recipe', response.data)
        self.assertIn(b'Tacos', response.data)
        response = app_client.post('/edit/3',
                                   buffered=True,
                                   content_type='multipart/form-data',
                                   data={'recipe_title': 'Tacos2',
                                         'recipe_description': 'Ground beef tacos',
                                         'recipe_type': 'Lunch',
                                         'recipe_public': 'True',
                                         'recipe_rating': '8',
                                         'recipe_steps': 'Step 1 Step 2 Step 3',
                                         'recipe_ingredients': 'Ingredient #1 Ingredient #2',
                                         'recipe_inspiration': 'http://www.foodnetwork.com/blaa',
                                         'recipe_dairy_free': 'True',
                                         'recipe_soy_free': 'True',
                                         'recipe_image': (BytesIO(b'my file contents'), 'image001.jpg')},
                                   follow_redirects=True)
        self.assertIn(b'Recipe has been updated for Tacos2.', response.data)


if __name__ == "__main__":
    unittest.main()
