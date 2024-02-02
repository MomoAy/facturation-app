from flask import Flask,redirect,url_for,render_template,request
from urllib.parse import quote_plus
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
db = SQLAlchemy()
mail = Mail()


def create_app():
    app=Flask(__name__)
    
    app.config["SECRET_KEY"] = "Some_key"
    
    password = quote_plus('1994')
    chaine = "postgresql://postgres:{}@localhost:5432/ecom".format(password)
    app.config["SQLALCHEMY_DATABASE_URI"] = chaine


    db.init_app(app)
    migrate = Migrate(app, db)
    
    from .auth import auth
    from .views_admin import views_admin
    from .views_client import views_client
    from .models import Utilisateur
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Utilisateur.query.get(int(id))
    
    with app.app_context(): 
        db.create_all()
    
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(views_admin, url_prefix="/admin")
    app.register_blueprint(views_client, url_prefix="/client")
    
    @app.route('/')
    def default_route():
        return redirect(url_for('auth.login'))

    
    return app
