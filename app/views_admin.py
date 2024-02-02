from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_required,  current_user
list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
from . import db

views_admin = Blueprint('views_admin',__name__)
