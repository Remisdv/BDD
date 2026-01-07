"""
CRUD pour la table mouvements_stock avec SQLAlchemy
"""

from connexion import get_session
from models import MouvementStock, Produit


def entree_stock(produit_id, quantite, motif=None):
    """Enregistrer une entrée de stock"""
    session = get_session()
    try:
        # Vérifier que le produit existe
        produit = session.query(Produit).filter(Produit.id == produit_id).first()
        if not produit:
            print("Produit non trouvé")
            return None
        
        # Créer le mouvement
        mouvement = MouvementStock(
            produit_id=produit_id,
            type_mouvement='ENTREE',
            quantite=quantite,
            motif=motif
        )
        session.add(mouvement)
        
        # Mettre à jour le stock du produit
        produit.quantite_stock += quantite
        
        session.commit()
        return mouvement.id
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'entrée de stock: {e}")
        return None
    finally:
        session.close()


def sortie_stock(produit_id, quantite, motif=None):
    """Enregistrer une sortie de stock"""
    session = get_session()
    try:
        # Vérifier que le produit existe
        produit = session.query(Produit).filter(Produit.id == produit_id).first()
        if not produit:
            print("Produit non trouvé")
            return None
        
        # Vérifier le stock disponible
        if produit.quantite_stock < quantite:
            print(f"Stock insuffisant. Disponible: {produit.quantite_stock}")
            return None
        
        # Créer le mouvement
        mouvement = MouvementStock(
            produit_id=produit_id,
            type_mouvement='SORTIE',
            quantite=quantite,
            motif=motif
        )
        session.add(mouvement)
        
        # Mettre à jour le stock du produit
        produit.quantite_stock -= quantite
        
        session.commit()
        return mouvement.id
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la sortie de stock: {e}")
        return None
    finally:
        session.close()


def lire_mouvements(limite=50):
    """Lire les derniers mouvements de stock"""
    session = get_session()
    try:
        mouvements = session.query(MouvementStock).order_by(
            MouvementStock.date_mouvement.desc()
        ).limit(limite).all()
        
        result = []
        for m in mouvements:
            result.append((
                m.id,
                m.produit.reference if m.produit else None,
                m.produit.nom if m.produit else None,
                m.type_mouvement,
                m.quantite,
                m.motif,
                m.date_mouvement
            ))
        return result
    finally:
        session.close()


def historique_produit(produit_id):
    """Obtenir l'historique des mouvements d'un produit"""
    session = get_session()
    try:
        mouvements = session.query(MouvementStock).filter(
            MouvementStock.produit_id == produit_id
        ).order_by(MouvementStock.date_mouvement.desc()).all()
        
        return [(m.id, m.type_mouvement, m.quantite, m.motif, m.date_mouvement) for m in mouvements]
    finally:
        session.close()
