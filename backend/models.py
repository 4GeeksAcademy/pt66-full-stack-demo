from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


"""
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(
        String(64),
        unique=True,
        nullable=False
    )
    password = Column(String(128), nullable=False)
    photos = relationship(
        "Photos",
        back_populates="user",
        uselist=True
    )
    comments = relationship(
        "Comment",
        back_populates="user",
        uselist=True
    )
"""


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    photos = db.relationship(
        "backend.models.Photo",
        back_populates="user",
        uselist=True
    )
    # comments = db.relationship(
    #     "Comment",
    #     back_populates="user",
    #     uselist=True
    # )
    collections = db.relationship(
        "backend.models.Collection",
        back_populates="user",
        uselist=True
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
        }


class Photo(db.Model):
    __tablename__ = "photos"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    user = db.relationship(
        "backend.models.User",
        back_populates="photos",
        uselist=False
    )
    # comments = db.relationship(
    #     "Comment",
    #     back_populates="photo",
    #     uselist=True
    # )
    url = db.Column(db.String(128))


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    # user = db.relationship(
    #     "User",
    #     back_populates="comments",
    #     uselist=False
    # )
    photo_id = db.Column(
        db.Integer,
        db.ForeignKey('photos.id')
    )
    # photo = db.relationship(
    #     "Photo",
    #     back_populates="comments",
    #     uselist=False
    # )
    text = db.Column(db.String(512))


class Collection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    user = db.relationship(
        "backend.models.User",
        back_populates="collections",
        uselist=False
    )


