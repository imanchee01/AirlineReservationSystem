from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:rootpassword@127.0.0.1/airline"

db = SQLAlchemy(app)


def init_db(app):
    class User(db.Model):
        __tablename__ = "user"

        UserId = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String(80), unique=True, nullable=False)
        user_email = db.Column(db.String(120), unique=True, nullable=False)
        user_password = db.Column(db.String(128), nullable=False)
        user_type = db.Column(db.String(50), nullable=False)

        def __init__(self, user_name, user_email, user_password, user_type):
            self.user_name = user_name
            self.user_email = user_email
            self.user_type = user_type
            self.set_password(user_password)

        def set_password(self, user_password):
            self.user_password = generate_password_hash(user_password)

        def check_password(self, user_password):
            return check_password_hash(self.user_password, user_password)

        def __repr__(self):
            return f"<User {self.user_name}>"


user = "root"
password = "rootpassword"
host = "127.0.0.1"
port = 3306
database = "airline"


def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


if __name__ == "__main__":

    try:
        engine = get_connection()
        print(f"Connection to the {host} for user {user} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
