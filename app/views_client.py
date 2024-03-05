import io
import json
import os
import smtplib
import ssl
import time
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

import pdfkit
import pywhatkit
import requests
from flask import (Blueprint, flash, make_response, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required
from pdf2image import convert_from_path
from weasyprint import HTML
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import DetailFacture, Facture, Produit

# import imgkit
# import base64
# import aspose.words as aw
# import subprocess



views_client = Blueprint('views_client', __name__)


@views_client.route("/")
@login_required
def home():
    print(session)
    all_products = Produit.query.all()
    return render_template("client/Home.html", all_products=all_products, user=current_user)

@views_client.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Produit.query.get(product_id)
    product_id = str(product_id)

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'quantity': 1, 'name': product.nom, 'price': float(product.prix), 'image': product.image}

    flash(f"{product.nom} a été ajouté à votre panier.", 'success')
    return redirect(url_for("views_client.home"))

@views_client.route('/view_cart')
@login_required
def view_cart():
    cart = session.get('cart', {})
    total_price = sum(item['quantity'] * item['price'] for item in cart.values())
    return render_template('client/Cart.html', cart=cart, total_price=round(total_price, 2))

@views_client.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash("Votre panier a été vidé.", 'success')
    return redirect(url_for("views_client.view_cart"))

@views_client.route("/checkout")
@login_required
def checkout():
    cart = session.get('cart', {})
    total_price = sum(item['quantity'] * item['price'] for item in cart.values())

    new_facture = Facture(
        libelle="Facture pour {}".format(current_user.nom),
        date_creation=datetime.utcnow(),
        utilisateur_id=current_user.id
    )
    db.session.add(new_facture)
    db.session.commit()

    # Ajouter les détails de la facture
    for product_id, item in cart.items():
        product = Produit.query.get(product_id)
        new_detail_facture = DetailFacture(
            facture_id=new_facture.id,
            produit_id=product.id,
            quantite=item['quantity']
        )
        db.session.add(new_detail_facture)
    db.session.commit()
    flash("Paiement enregistré avec succès", "success")
    return render_template('client/facture.html', facture=new_facture, cart=cart, total_price=round(total_price, 2))

@views_client.route("/remove_item/<item_id>")
def remove_item(item_id):
    cart = session.get('cart', {})
    
    if item_id in cart:
        del cart[item_id]
        session['cart'] = cart

    flash("Element removed with success", "success")
    return redirect(url_for("views_client.view_cart"))


@views_client.route("/validate")
@login_required
def validate():
    cart = session.get('cart', {})
    total_price = round(sum(item['quantity'] * float(item['price']) for item in cart.values()), 2)
    date_creation = datetime.utcnow()

    pdf_filename = f"invoice_{date_creation.strftime('%Y%m%d%H%M%S')}.pdf"

    pdf_path = os.path.join("E:\\Users\\AYEVA\\Desktop\\Programmation Distribué\\pdfFile", pdf_filename)

    # Génération du PDF avec WeasyPrint
    html_content = render_template('client/facture_envoie.html', date=date_creation, cart=cart, total_price=total_price)
    HTML(string=html_content).write_pdf(pdf_path)

    send_email_with_attachment(current_user.email, 'Votre facture', 'Veuillez trouver votre facture en pièce jointe.', pdf_path)

    send_whatsapp_message(current_user.telephone, pdf_path)

    session.pop('cart', None)

    flash("Your invoice has been sent directly to your address.", "success")

    return redirect(url_for("views_client.home"))


def send_email_with_attachment(to_email, subject, body, attachment_path):
    sender_email = 'mohamed.ayeva.123@gmail.com'
    sender_password = ''#Je pourrais retrouver le code sur chat gpt ou la copie envoyer à thierno sur telegram

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    with io.open(attachment_path, 'rb') as attachment:
        base = MIMEBase('application', 'octet-stream')
        base.set_payload(attachment.read())
        encoders.encode_base64(base)
        base.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        message.attach(base)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
        server.login(sender_email, sender_password)

        text = MIMEText(body, 'plain', _charset='utf-8')
        message.attach(text)

        server.sendmail(sender_email, to_email, message.as_string().encode('utf-8'))



def send_whatsapp_message(to_number, pdf_path):
    try:
        image_folder = 'E:\\Users\\AYEVA\\Desktop\\Programmation Distribué\\imageFile'

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        image_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.png'

        image_path = os.path.join(image_folder, image_filename)

        images = convert_from_path(pdf_path, 300)
        
        images[0].save(image_path, 'PNG')

        kit.sendwhats_image(f"+{to_number}", image_path)
    except Exception as e:
        print("Error", e)