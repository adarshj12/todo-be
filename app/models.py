from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db= SQLAlchemy()

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