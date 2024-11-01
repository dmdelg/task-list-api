from flask import Blueprint, abort, make_response, request, Response, jsonify
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    
    title = request_body.get("title")
    description = request_body.get("description")

    # Validate input
    if not title or not description:
        return {"details": "Invalid data"}, 400

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return {"task": {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
    }}, 201

@tasks_bp.get("")
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    } for task in tasks]), 200

@tasks_bp.get("/<int:task_id>")
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404
    
    return {"task": {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    }}, 200

@tasks_bp.put("/<int:task_id>")
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")

    # Update attributes
    task.title = title
    task.description = description
    db.session.commit()

    return {"task": {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }}, 200

@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200
