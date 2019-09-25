from flask import Flask
from config import Config
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import  Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from flask import request
from webapp.auth import bp as auth_bp, routes

app = Flask (__name__)
app.config.from_object(Config)
app.register_blueprint (auth_bp,url_prefix= '/auth' )
db = SQLAlchemy ()
migrate= Migrate()
login=LoginManager()
login.login_view='auth.login'
mail = Mail()
babel=Babel()

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
def creat_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    return app
    
    from webapp import models