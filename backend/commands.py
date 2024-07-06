
import json
import click
from backend.models import db, User, Photo

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""


def setup_commands(app):
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users")  # name of our command
    @click.argument("count")  # argument of out command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")

    @app.cli.command("popdb")
    def popdb():
        users = []
        with open("./backend/test_users.json", "rt") as user_data:
            users = json.load(user_data)
        
        for user in users:
            db.session.add(User(**user))
        db.session.commit()

        photos = []
        with open("./backend/test_photos.json", "rt") as photo_data:
            photos = json.load(photo_data)

        for photo in photos:
            user = User.query.filter_by(username=photo["user"]).first()
            db.session.merge(Photo(
                user_id=user.id,
                url=photo["url"]
            ))
        db.session.commit()
