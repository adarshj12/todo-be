from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    password = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False,unique=True)

    def __repr__(self):
        return f'<User {self.name}>'