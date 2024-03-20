import os  

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 


