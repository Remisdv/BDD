"""
CRUD pour la table utilisateurs avec SQLAlchemy
Gestion de l'authentification
"""

import hashlib
from connexion import get_session
from models import Utilisateur


def hasher_mot_de_passe(mot_de_passe):
    """Hasher un mot de passe avec SHA256"""
    return hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()


def creer_utilisateur(username, mot_de_passe, role='user'):
    """Créer un nouvel utilisateur"""
    session = get_session()
    try:
        # Vérifier si le username existe déjà
        existant = session.query(Utilisateur).filter(Utilisateur.username == username).first()
        if existant:
            print("Ce nom d'utilisateur existe déjà")
            return None
        
        password_hash = hasher_mot_de_passe(mot_de_passe)
        utilisateur = Utilisateur(
            username=username,
            password_hash=password_hash,
            role=role
        )
        session.add(utilisateur)
        session.commit()
        return utilisateur.id
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        session.close()


def authentifier(username, mot_de_passe):
    """Authentifier un utilisateur"""
    session = get_session()
    try:
        password_hash = hasher_mot_de_passe(mot_de_passe)
        utilisateur = session.query(Utilisateur).filter(
            Utilisateur.username == username,
            Utilisateur.password_hash == password_hash,
            Utilisateur.actif == True
        ).first()
        
        if utilisateur:
            return (utilisateur.id, utilisateur.username, utilisateur.role)
        return None
    finally:
        session.close()


def lire_utilisateurs():
    """Lire tous les utilisateurs"""
    session = get_session()
    try:
        utilisateurs = session.query(Utilisateur).order_by(Utilisateur.username).all()
        return [(u.id, u.username, u.role, u.actif) for u in utilisateurs]
    finally:
        session.close()


def lire_utilisateur(utilisateur_id):
    """Lire un utilisateur par son ID"""
    session = get_session()
    try:
        u = session.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if u:
            return (u.id, u.username, u.role, u.actif)
        return None
    finally:
        session.close()


def modifier_mot_de_passe(utilisateur_id, nouveau_mot_de_passe):
    """Modifier le mot de passe d'un utilisateur"""
    session = get_session()
    try:
        utilisateur = session.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if utilisateur:
            utilisateur.password_hash = hasher_mot_de_passe(nouveau_mot_de_passe)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        session.close()


def admin_existe():
    """Vérifie si au moins un utilisateur admin actif existe."""
    session = get_session()
    try:
        count = session.query(Utilisateur).filter(Utilisateur.role == 'admin', Utilisateur.actif == True).count()
        session.close()
        return count > 0
    except Exception as e:
        print(f"Erreur lors de la vérification de l'admin: {e}")
        session.close()
        return False


def modifier_role(utilisateur_id, nouveau_role):
    """Modifier le rôle d'un utilisateur"""
    session = get_session()
    try:
        if nouveau_role not in ('admin', 'user'):
            print("Rôle invalide. Utilisez 'admin' ou 'user'.")
            return False
        
        utilisateur = session.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if utilisateur:
            utilisateur.role = nouveau_role
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        session.close()


def desactiver_utilisateur(utilisateur_id):
    """Désactiver un utilisateur"""
    session = get_session()
    try:
        utilisateur = session.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if utilisateur:
            utilisateur.actif = False
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la désactivation: {e}")
        return False
    finally:
        session.close()


def activer_utilisateur(utilisateur_id):
    """Activer un utilisateur"""
    session = get_session()
    try:
        utilisateur = session.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if utilisateur:
            utilisateur.actif = True
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'activation: {e}")
        return False
    finally:
        session.close()


def supprimer_utilisateur(utilisateur_id):
    """Supprimer un utilisateur"""
    session = get_session()
    try:
        utilisateur = session.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if utilisateur:
            session.delete(utilisateur)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        session.close()


def compter_utilisateurs():
    """Compter le nombre d'utilisateurs"""
    session = get_session()
    try:
        return session.query(Utilisateur).count()
    finally:
        session.close()
