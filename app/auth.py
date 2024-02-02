from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Utilisateur
from . import db


auth = Blueprint('auth',__name__)


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET" :
        return render_template("auth/Register.html")
    else:
        nom = request.form.get("name")
        telephone = request.form.get("tel")
        email=  request.form.get("email")
        mot_de_passe = request.form.get("password")
        repeat_password = request.form.get("repeat_password")

       
        user = Utilisateur.query.filter_by(email=email).first()
        user2 = Utilisateur.query.filter_by(telephone=telephone).first()
        if user or user2: 
                flash("Email or Username already exist", category="error")
                return redirect(url_for("auth.signup"))
        elif len(telephone) < 8:
                flash("Number must be greater than 8 characters.", category="error")
                return redirect(url_for("auth.signup"))
        elif len(email) < 4 :
                flash("Email must be greater than 4 characters.", category="error")
                return redirect(url_for("auth.signup"))
        elif nom is None or len(nom) < 4 : 
                flash("Name must be greater than 4 characters.", category="error")
                return redirect(url_for("auth.signup"))
        elif mot_de_passe != repeat_password :
                flash("Password don't match.", category="error")
                return redirect(url_for("auth.signup"))
        elif len(mot_de_passe) < 7 :
                flash("Password must be greater than 7 characters.", category="error")
                return redirect(url_for("auth.signup"))
        else:
                new_user = Utilisateur(nom = nom, telephone = telephone, email=email, mot_de_passe = generate_password_hash(mot_de_passe, method="scrypt"), isAdmin = False)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created", category="success")
                return redirect(url_for("auth.login"))
  

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/Login.html")
    else:
        email = request.form.get("email")
        mot_de_passe = request.form.get("password")
        user = Utilisateur.query.filter_by(email = email).first()
        if not user or not check_password_hash(user.mot_de_passe, mot_de_passe) :
            flash("Vérifier vos informations de connection", category="error")
            return redirect(url_for("auth.login"))
        elif user : 
            if user.isAdmin == True : 
                login_user(user)
                flash("Welcome Administrator "+ user.nom, category="success")
                return redirect(url_for("views_admin.home"))
            elif user.isAdmin == False : 
                login_user(user)
                flash("Successful connection, Welcome "+ user.nom, category="success")
                return redirect(url_for("views_client.home"))
            
@auth.route("/logout")
@login_required
def logout():
    session.pop('cart', None)
    logout_user()
    flash("Successful disconnection", category="success")
    return redirect(url_for("auth.login"))





