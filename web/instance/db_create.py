# Check the PYTHONPATH environment variable before beginning to ensure that the
# top-level directory is included.  If not, append the top-level.  This allows
# the modules within the .../project/ directory to be discovered.
import sys
import os

print('Creating database tables.')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    sys.path.append(os.path.abspath(os.curdir))


# Create the database tables, add some initial data, and commit to the database
from project import db
from project.models import Vitamin, Screening, User
import pandas as pd
from os import getcwd


path = getcwd() + "/instance/vitamins.csv"
vitamins_db = pd.read_csv(path)
vitamins = []
for index, row in vitamins_db.iterrows():
    v = Vitamin(row["name"], row["mobility"], row["stability"],
                      row["target_area"], row["description"], row["link"])
    vitamins.append(v)

# Drop all of the existing database tables
db.drop_all()

# Create the database and the database table
db.create_all()

# Insert user data
user1 = User(email='partees21@gmail.com', plaintext_password='password', role='user')
db.session.add(user1)

# Commit the changes for the users
db.session.commit()

# insert Vitamins
for v in vitamins:
    db.session.add(v)

# Commit the changes for the recipes
db.session.commit()

print('...done!')
