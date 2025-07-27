from flask import Blueprint, request, make_response
from app.models import Todo,db
from app.middlewares.verifyToken import verify_token

todos_bp = Blueprint('todos', __name__, url_prefix='/todos')

@todos_bp.route('/', methods=['POST'])
@verify_token
def create_todo(current_user):
    data = request.json
    todo = Todo(activity=data['activity'], userId=current_user.id)
    db.session.add(todo)
    db.session.commit()
    return make_response({"msg": "Todo added"}, 201)

@todos_bp.route('/', methods=['GET'])
@verify_token
def get_todos(current_user):
    todos = Todo.query.filter_by(userId=current_user.id).all()
    return make_response([{"id": t.id, "activity": t.activity, "completed": t.completed} for t in todos])

@todos_bp.route('/<int:id>', methods=['PATCH'])
@verify_token
def update_todo(current_user,id):
    todo = Todo.query.filter_by(id=id, userId=current_user.id).first()
    if todo:
        # data = request.json
        # if data['activity']:
        #     todo.activity = data['activity']
        # if data['activity']:
        #     todo.completed = data.get('completed', todo.completed)
        todo.completed = not todo.completed
        db.session.commit()
        return make_response({"msg": "Todo updated"},200)
    else:
        return make_response({"msg": "Todo not found"},404)

@todos_bp.route('/<int:id>', methods=['DELETE'])
@verify_token
def delete_todo(current_user,id):
    todo = Todo.query.filter_by(id=id, userId=current_user.id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return make_response({"msg": "Todo deleted"},200)
    else:
        return make_response({"msg": "Todo not found"},404)