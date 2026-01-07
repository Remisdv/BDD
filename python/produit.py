"""
CRUD pour la table produits avec SQLAlchemy
"""

from sqlalchemy import or_
from connexion import get_session
from models import Produit, Categorie, Fournisseur


def creer_produit(reference, nom, prix_unitaire, description=None, 
                  quantite_stock=0, seuil_alerte=10, categorie_id=None, fournisseur_id=None):
    """Créer un nouveau produit"""
    session = get_session()
    try:
        produit = Produit(
            reference=reference,
            nom=nom,
            description=description,
            prix_unitaire=prix_unitaire,
            quantite_stock=quantite_stock,
            seuil_alerte=seuil_alerte,
            categorie_id=categorie_id,
            fournisseur_id=fournisseur_id
        )
        session.add(produit)
        session.commit()
        return produit.id
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        session.close()


def lire_produits():
    """Lire tous les produits avec catégorie et fournisseur"""
    session = get_session()
    try:
        produits = session.query(Produit).order_by(Produit.nom).all()
        result = []
        for p in produits:
            result.append((
                p.id,
                p.reference,
                p.nom,
                p.prix_unitaire,
                p.quantite_stock,
                p.seuil_alerte,
                p.categorie.nom if p.categorie else None,
                p.fournisseur.nom if p.fournisseur else None
            ))
        return result
    finally:
        session.close()


def lire_produit(produit_id):
    """Lire un produit par son ID"""
    session = get_session()
    try:
        p = session.query(Produit).filter(Produit.id == produit_id).first()
        if p:
            return (
                p.id,
                p.reference,
                p.nom,
                p.description,
                p.prix_unitaire,
                p.quantite_stock,
                p.seuil_alerte,
                p.categorie.nom if p.categorie else None,
                p.fournisseur.nom if p.fournisseur else None
            )
        return None
    finally:
        session.close()


def rechercher_produits(terme):
    """Rechercher des produits par nom ou référence"""
    session = get_session()
    try:
        pattern = f"%{terme}%"
        produits = session.query(Produit).filter(
            or_(Produit.nom.ilike(pattern), Produit.reference.ilike(pattern))
        ).order_by(Produit.nom).all()
        
        result = []
        for p in produits:
            result.append((
                p.id,
                p.reference,
                p.nom,
                p.prix_unitaire,
                p.quantite_stock,
                p.seuil_alerte,
                p.categorie.nom if p.categorie else None,
                p.fournisseur.nom if p.fournisseur else None
            ))
        return result
    finally:
        session.close()


def modifier_produit(produit_id, **kwargs):
    """Modifier un produit existant"""
    session = get_session()
    try:
        produit = session.query(Produit).filter(Produit.id == produit_id).first()
        if not produit:
            return False
        
        champs_autorises = ['reference', 'nom', 'description', 'prix_unitaire', 
                           'quantite_stock', 'seuil_alerte', 'categorie_id', 'fournisseur_id']
        
        for champ, valeur in kwargs.items():
            if champ in champs_autorises and valeur is not None:
                setattr(produit, champ, valeur)
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        session.close()


def supprimer_produit(produit_id):
    """Supprimer un produit"""
    session = get_session()
    try:
        produit = session.query(Produit).filter(Produit.id == produit_id).first()
        if produit:
            session.delete(produit)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        session.close()


def produits_en_alerte():
    """Obtenir les produits dont le stock est sous le seuil d'alerte"""
    session = get_session()
    try:
        produits = session.query(Produit).filter(
            Produit.quantite_stock <= Produit.seuil_alerte
        ).order_by(Produit.quantite_stock).all()
        
        result = []
        for p in produits:
            result.append((
                p.id,
                p.reference,
                p.nom,
                p.quantite_stock,
                p.seuil_alerte,
                p.categorie.nom if p.categorie else None
            ))
        return result
    finally:
        session.close()


def produits_par_categorie(categorie_id):
    """Obtenir les produits d'une catégorie"""
    session = get_session()
    try:
        produits = session.query(Produit).filter(
            Produit.categorie_id == categorie_id
        ).order_by(Produit.nom).all()
        
        return [(p.id, p.reference, p.nom, p.prix_unitaire, p.quantite_stock) for p in produits]
    finally:
        session.close()
