from flask import Flask
from dotenv import load_dotenv
import os
from app.models import db
from app.auth.routes import auth_bp
from app.todo.routes import todos_bp

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 

app.register_blueprint(auth_bp)  
app.register_blueprint(todos_bp)


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1',port=os.getenv('PORT'),debug=True)
