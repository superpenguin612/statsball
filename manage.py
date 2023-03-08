import os
from flask_script import Manager
from flask_migrate import Migrate

from app import app, db

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DATABASE_URL'] = 'postgres://jhamuqwxgfbheq:a4055f23125991014264ad1060b05ecab13eddf26236980b4011bb631965bc23@ec2-174-129-224-157.compute-1.amazonaws.com:5432/d62mab0iossfp4'

migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()