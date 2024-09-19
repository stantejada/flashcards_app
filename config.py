import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_guess'
    FILE_UPLOAD = os.path.join(basedir, 'app','static', 'img')
    MAX_CONTENT_LENGTH = 16*1024*1024
    ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
    
class Development(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    
class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'site.db')