"""
CRUD pour la table fournisseurs avec SQLAlchemy
"""

from connexion import get_session
from models import Fournisseur


def creer_fournisseur(nom, email=None, telephone=None, adresse=None):
    """Créer un nouveau fournisseur"""
    session = get_session()
    try:
        fournisseur = Fournisseur(nom=nom, email=email, telephone=telephone, adresse=adresse)
        session.add(fournisseur)
        session.commit()
        return fournisseur.id
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        session.close()


def lire_fournisseurs():
    """Lire tous les fournisseurs"""
    session = get_session()
    try:
        fournisseurs = session.query(Fournisseur).order_by(Fournisseur.nom).all()
        return [(f.id, f.nom, f.email, f.telephone, f.adresse) for f in fournisseurs]
    finally:
        session.close()


def lire_fournisseur(fournisseur_id):
    """Lire un fournisseur par son ID"""
    session = get_session()
    try:
        f = session.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).first()
        if f:
            return (f.id, f.nom, f.email, f.telephone, f.adresse)
        return None
    finally:
        session.close()


def modifier_fournisseur(fournisseur_id, nom=None, email=None, telephone=None, adresse=None):
    """Modifier un fournisseur existant"""
    session = get_session()
    try:
        fournisseur = session.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).first()
        if not fournisseur:
            return False
        
        if nom is not None:
            fournisseur.nom = nom
        if email is not None:
            fournisseur.email = email
        if telephone is not None:
            fournisseur.telephone = telephone
        if adresse is not None:
            fournisseur.adresse = adresse
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        session.close()


def supprimer_fournisseur(fournisseur_id):
    """Supprimer un fournisseur"""
    session = get_session()
    try:
        fournisseur = session.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).first()
        if fournisseur:
            session.delete(fournisseur)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        session.close()
