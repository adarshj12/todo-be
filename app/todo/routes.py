from flask import Blueprint, request, make_response
from app.models import Todo,db

todos_bp = Blueprint('todos', __name__, url_prefix='/todos')

@todos_bp.route('/', methods=['POST'])
def create_todo(current_user):
    data = request.get_json()
    todo = Todo(activity=data['activity'], userId=current_user.id)
    db.session.add(todo)
    db.session.commit()
    return make_response({"msg": "Todo added"}, 201)

@todos_bp.route('/', methods=['GET'])
def get_todos(current_user):
    todos = Todo.query.filter_by(userId=current_user.id).all()
    return make_response([{"id": t.id, "activity": t.activity, "completed": t.completed} for t in todos])

@todos_bp.route('/<int:id>', methods=['PUT'])
def update_todo(current_user,id):
    todo = Todo.query.filter_by(id=id, userId=current_user.id).first()
    if todo:
        data = request.get_json()
        todo.task = data['task']
        todo.completed = data.get('completed', todo.completed)
        db.session.commit()
        return make_response({"msg": "Todo updated"},200)
    else:
        return make_response({"msg": "Todo not found"},404)

@todos_bp.route('/<int:id>', methods=['DELETE'])
def delete_todo(current_user,id):
    todo = Todo.query.filter_by(id=id, userId=current_user.id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return make_response({"msg": "Todo deleted"},200)
    else:
        return make_response({"msg": "Todo not found"},404)