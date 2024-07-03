"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from backend.models import db, User
from flask_cors import CORS

api = Blueprint('api', __name__, url_prefix="/api")

# Allow CORS requests to this API
CORS(api)


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
        return jsonify(message="User already exists"), 400
    
    user = User(
        username=body["username"],
        password=body["password"]
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(user.serialize())


# @api.route("/users", methods=["GET"])
# def read_users():
#     photo_users = []
#     for user in users:
#         photo_users.append({
#             **user,
#             "photos": list(filter(
#                 lambda photo: photo["user_id"] == user["id"],
#                 photos
#             ))
#         })
#     return jsonify(users=photo_users)


# @api.route("/photos", methods=["POST"])
# def create_photo():
#     """
#     Body:
#     {
#         "url": "https://wob.site/photo.jpg",
#         "user_id": 1
#     }
#     """
#     data = request.json
#     if data["user_id"] not in [u["id"] for u in users]:
#         return jsonify(msg="User does not exist."), 404
#     photo = {
#         **data,
#         "id": len(photos) + 1
#     }
#     photos.append(photo)
#     return jsonify(photo)