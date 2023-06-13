
from flask import Flask, render_template, url_for,flash,redirect,request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
#from flask_mail import Mail
from app.config import Config
import os
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
# Initialize Flask App




cred = credentials.Certificate('C:/Users/user/Desktop/Micro service AMS V2/planning2/project/app/key.json')
default_app = initialize_app(cred,{'storageBucket': 'dbedl-a5053.appspot.com'})
db = firestore.client()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")

   
    bcrypt.init_app(app)
    
    
    
    from app.entity.User.route import user
    from app.entity.RDV.route import rdv
    from app.entity.Participant.route import participant
    from app.entity.EDL.route import edl
    
    app.register_blueprint(user)
    app.register_blueprint(rdv)
    app.register_blueprint(participant)
    app.register_blueprint(edl)
    return app