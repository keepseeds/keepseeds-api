import os
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

DB_KEY = 'DATABASE_URL'
DB_LOCAL_PATH = 'postgresql://localhost/andy'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(DB_KEY, DB_LOCAL_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from db import db
from models import *
from models.enums import TokenType

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
