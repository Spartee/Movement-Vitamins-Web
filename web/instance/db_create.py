# Check the PYTHONPATH environment variable before beginning to ensure that the
# top-level directory is included.  If not, append the top-level.  This allows
# the modules within the .../project/ directory to be discovered.
import sys
import os

print('Creating database tables for Family Recipes app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    sys.path.append(os.path.abspath(os.curdir))


# Create the database tables, add some initial data, and commit to the database
from project import db
from project.models import Recipe, User


# Drop all of the existing database tables
db.drop_all()

# Create the database and the database table
db.create_all()

# Insert user data
user1 = User(email='patkennedy79@yahoo.com', plaintext_password='password1234', role='user')
user2 = User(email='kennedyfamilyrecipes@gmail.com', plaintext_password='PaSsWoRd', role='user')
user3 = User(email='blaa@blaa.com', plaintext_password='MyFavPassword', role='user')
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit the changes for the users
db.session.commit()

# Insert recipe data
recipe1 = Recipe('Slow-Cooker Tacos', 'Delicious ground beef that has been simmering in taco seasoning and sauce.  Perfect with hard-shelled tortillas!', user2.id, False)
recipe2 = Recipe('Hamburgers', 'Classic dish elevated with pretzel buns.', user2.id, True)
recipe3 = Recipe('Mediterranean Chicken', 'Grilled chicken served with pitas, hummus, and sauted vegetables.', user2.id, True)
db.session.add(recipe1)
db.session.add(recipe2)
db.session.add(recipe3)

# Commit the changes for the recipes
db.session.commit()

print('...done!')
