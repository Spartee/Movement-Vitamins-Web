
## Overview

The web interface for the Movement Vitamins application.


## How to Run (Development)

1. Create the Dockerfile for the postgres service

- % cd ./flask_recipe_app/web/
- % python create_postgres_dockerfile.py
- % cd ..

2. Build and run the Docker containers

- % docker-compose build
- % docker-compose up -d

3. Create or re-initialize the database

- % docker-compose run --rm web python ./instance/db_create.py

Go to your favorite web browser and open:
    http://192.168.99.100:5000  $ Check the IP address using 'docker-machine ip'

## Key Python Modules Used

- Flask - web framework
- Jinga2 - templating engine
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Bcrypt - password hashing
- Flask-Login - support for user management
- Flask-Migrate - database migrations
- Flask-WTF - simplifies forms
- itsdangerous - helps with user management, especially tokens

This application is written using Python 3.6.1.  The database used is PostgreSQL.

Docker is the recommended tool for running in development and production.

## Unit Testing

In the top-level folder:
    % nose2

