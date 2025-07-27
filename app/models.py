from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db= SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    password = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False,unique=True)

    def __repr__(self):
        return f'<User {self.name}>'

class Todo(db.Model):
    __tablename__='todos'
    id = db.Column(db.Integer,primary_key=True)
    activity = db.Column(db.Text,nullable=False)
    completed = db.Column(db.Boolean,nullable=False,default=False)
    userId = db.Column(db.Text,db.ForeignKey("User.id"))
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())

    @property
    def serialize(self):

        return {
            "id":self.id,
            "activity":self.activity,
            "created_at":self.created_at
        }
