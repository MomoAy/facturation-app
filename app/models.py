from . import db
from flask_login import UserMixin

class Utilisateur(db.Model, UserMixin):
    __tablename__ = "utilisateur"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(250), nullable=False)
    telephone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(250), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable = False)
    facture = db.relationship("Facture", backref="utilisateur", lazy = True)

    
class Produit(db.Model):
    __tablename__ = "produit"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(250), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    
class DetailCommande(db.Model):
    __tablename__ = 'detailcommande'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"))
    produit_id = db.Column(db.Integer, db.ForeignKey("produit.id"))
    quantite = db.Column(db.Integer, nullable = False)
    dateCommande = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    
    utilisateur = db.relationship('Utilisateur', backref=db.backref('commandes_detailCommande', lazy=True))
    produit = db.relationship('Produit', backref=db.backref('commandes_detailCommande', lazy=True))
    
class Facture(db.Model):
    __tablename__ = "facture"
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(255), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    
class DetailFacture(db.Model):
    __tablename__ = 'detailfacture'
    id = db.Column(db.Integer, primary_key=True)
    facture_id = db.Column(db.Integer, db.ForeignKey("facture.id"))
    produit_id = db.Column(db.Integer, db.ForeignKey("produit.id"))
    quantite = db.Column(db.Integer, nullable = False)
    
    facture = db.relationship('Facture', backref=db.backref('commandes_detailFacture', lazy=True))
    produit = db.relationship('Produit', backref=db.backref('commandes_detailFacture', lazy=True))

