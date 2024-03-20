import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(script_info=None):
    load_dotenv()
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    # app.config['SECRET_KEY'] = 'my-secret-key'

    db.init_app(app)

    from src.api import api  
    api.init_app(app)  
    
    with app.app_context():
        db.metadata.create_all(bind=db.engine, checkfirst=True)

    return app