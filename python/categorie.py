"""
CRUD pour la table categories avec SQLAlchemy
"""

from connexion import get_session
from models import Categorie


def creer_categorie(nom, description=None):
    """Créer une nouvelle catégorie"""
    session = get_session()
    try:
        categorie = Categorie(nom=nom, description=description)
        session.add(categorie)
        session.commit()
        return categorie.id
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        session.close()


def lire_categories():
    """Lire toutes les catégories"""
    session = get_session()
    try:
        categories = session.query(Categorie).order_by(Categorie.nom).all()
        return [(c.id, c.nom, c.description) for c in categories]
    finally:
        session.close()


def lire_categorie(categorie_id):
    """Lire une catégorie par son ID"""
    session = get_session()
    try:
        c = session.query(Categorie).filter(Categorie.id == categorie_id).first()
        if c:
            return (c.id, c.nom, c.description)
        return None
    finally:
        session.close()


def modifier_categorie(categorie_id, nom=None, description=None):
    """Modifier une catégorie existante"""
    session = get_session()
    try:
        categorie = session.query(Categorie).filter(Categorie.id == categorie_id).first()
        if not categorie:
            return False
        
        if nom is not None:
            categorie.nom = nom
        if description is not None:
            categorie.description = description
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        session.close()


def supprimer_categorie(categorie_id):
    """Supprimer une catégorie"""
    session = get_session()
    try:
        categorie = session.query(Categorie).filter(Categorie.id == categorie_id).first()
        if categorie:
            session.delete(categorie)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        session.close()
