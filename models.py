from app import db
from sqlalchemy.dialects.postgresql import JSONB


class Entry(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(JSONB)

class Flat(db.Model):
    __tablename__ = 'flat'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(JSONB)


