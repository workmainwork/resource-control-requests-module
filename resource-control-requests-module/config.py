import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'coursework-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
TESTING = False
