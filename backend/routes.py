"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from backend.models import db, User, Photo
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token, current_user, jwt_required
)

api = Blueprint('api', __name__, url_prefix="/api")

# Allow CORS requests to this API
CORS(api)


@api.route("/login", methods=["POST"])
def login():
    """
    body:
    {
        "username": "sombra",
        "password": "littleblueparrot"
    }
    """
    body = request.json
    user: User | None = User.query.filter_by(
        username=body["username"]
    ).first()

    if not user:
        return jsonify(msg="Invalid credentials."), 401
    
    if user.password != body.get("password"):
        return jsonify(msg="Invalid credentials."), 401

    return jsonify(
        token=create_access_token(user)
    )


@api.route("/users", methods=["POST"])
def create_user():
    """
    body:
    {
        "username": "sombra",
        "password": "littleblueparrot"
    }
    """
    body = request.json

    # select * from `users` where username="sombra" limit 1;
    user: User | None = User.query.filter_by(
        username=body["username"]
    ).first()
    if user:
        return jsonify(msg="User already exists"), 400
    
    user = User(
        username=body["username"],
        password=body["password"]
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(user.serialize())


@api.route("/users/current", methods=["GET"])
@jwt_required()
def read_current_user():
    return jsonify(current_user.serialize(include_photos=True))


@api.route("/users", methods=["GET"])
def read_many_users():
    photo_users = User.query.all()
    return jsonify(users=[user.serialize(include_photos=True) for user in photo_users])


@api.route("/users/<string:username>", methods=["GET"])
def read_single_user(username):
    photo_user = User.query.filter_by(username=username).first()
    if not photo_user:
        return jsonify(msg="User does not exist."), 404
    return jsonify(photo_user.serialize(include_photos=True))


@api.route("/photos", methods=["POST"])
@jwt_required()
def create_photo():
    """
    Body:
    {
        "url": "https://wob.site/photo.jpg",
    }
    """
    data = request.json
    user = current_user

    if not user:
        return jsonify(msg="User does not exist."), 404
    
    photo = Photo(url=data.get("url"))
    user.photos.append(photo)
    db.session.merge(user)
    db.session.commit()
    db.session.refresh(photo)
    return jsonify(photo.serialize(include_user=True))


@api.route("/photos", methods=["GET"])
def read_many_photos():
    photos = Photo.query.all()
    return jsonify(photos=[photo.serialize(include_user=True) for photo in photos])


@api.route("/photos/<int:id>", methods=["GET"])
def read_single_photo(id: int):
    photo = Photo.query.filter_by(id=id).first()
    if not photo:
        return jsonify(msg="Photo does not exist."), 404
    return jsonify(photo.serialize(include_user=True))
    


@api.route("/photos/<int:id>", methods=["PUT"])
def update_photo(id: int):
    """
    Body:
    {
        "url": "https://wob.site/photo.jpg",
    }
    """
    photo = Photo.query.filter_by(id=id).first()
    data = request.json

    if not photo:
        return jsonify(msg="Photo does not exist."), 404
    
    photo.url = data.get("url")
    db.session.merge(photo)
    db.session.commit()
    db.session.refresh(photo)
    return jsonify(photo.serialize(include_user=True))


@api.route("/photos/<int:id>", methods=["DELETE"])
def delete_photo(id: int):
    photo = Photo.query.filter_by(id=id).first()

    if not photo:
        return jsonify(msg="Photo does not exist."), 404
    
    db.session.delete(photo)
    db.session.commit()
    return "", 204
