import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = "POO" 
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "datos.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 