#manage.py


import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime 

from project import app, db
from project.models import User, Role


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

#migrations
manager.add_command('db', MigrateCommand)

# Creates the db tables.
@manager.command
def create_db():
    db.create_all()


# Drops the db tables
@manager.command
def drop_db():
    db.drop_all()

# Creates admin user and admin role
@manager.command
def create_admin():
    user = User(email="", password="", username="", active=True, confirmed_at=datetime.utcnow())
    role = Role(name='admin')
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
