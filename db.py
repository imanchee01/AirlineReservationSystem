from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b"cvobidrnsuerbsifurf34ads"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:rootpassword@127.0.0.1/airline"

db.init_app(app)


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

    # TODO: user encryption!
    def set_password(self, user_password):
        self.user_password = user_password  # generate_password_hash(user_password)

    # TODO: user encryption!
    def check_password(self, user_password):
        return user_password == self.user_password  # check_password_hash(self.user_password, user_password)

    def __repr__(self):
        return f"<User {self.user_name}>"
