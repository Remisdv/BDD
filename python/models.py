"""
Modèles SQLAlchemy ORM pour la gestion de stock
"""

import uuid
from sqlalchemy import Column, String, Text, Integer, DECIMAL, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from connexion import Base


class Categorie(Base):
    """Modèle pour les catégories de produits"""
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    produits = relationship("Produit", back_populates="categorie")

    def __repr__(self):
        return f"<Categorie(nom='{self.nom}')>"


class Fournisseur(Base):
    """Modèle pour les fournisseurs"""
    __tablename__ = 'fournisseurs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(150), nullable=False)
    email = Column(String(100), unique=True)
    telephone = Column(String(20))
    adresse = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    produits = relationship("Produit", back_populates="fournisseur")

    def __repr__(self):
        return f"<Fournisseur(nom='{self.nom}')>"


class Produit(Base):
    """Modèle pour les produits"""
    __tablename__ = 'produits'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = Column(String(50), nullable=False, unique=True)
    nom = Column(String(200), nullable=False)
    description = Column(Text)
    prix_unitaire = Column(DECIMAL(10, 2), nullable=False)
    quantite_stock = Column(Integer, nullable=False, default=0)
    seuil_alerte = Column(Integer, default=10)
    categorie_id = Column(UUID(as_uuid=True), ForeignKey('categories.id', ondelete='SET NULL'))
    fournisseur_id = Column(UUID(as_uuid=True), ForeignKey('fournisseurs.id', ondelete='SET NULL'))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    categorie = relationship("Categorie", back_populates="produits")
    fournisseur = relationship("Fournisseur", back_populates="produits")
    mouvements = relationship("MouvementStock", back_populates="produit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Produit(ref='{self.reference}', nom='{self.nom}')>"


class MouvementStock(Base):
    """Modèle pour les mouvements de stock"""
    __tablename__ = 'mouvements_stock'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    produit_id = Column(UUID(as_uuid=True), ForeignKey('produits.id', ondelete='CASCADE'), nullable=False)
    type_mouvement = Column(String(10), nullable=False)  # 'ENTREE' ou 'SORTIE'
    quantite = Column(Integer, nullable=False)
    motif = Column(Text)
    date_mouvement = Column(TIMESTAMP, server_default=func.current_timestamp())
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    produit = relationship("Produit", back_populates="mouvements")

    def __repr__(self):
        return f"<MouvementStock(type='{self.type_mouvement}', qte={self.quantite})>"


class Utilisateur(Base):
    """Modèle pour les utilisateurs"""
    __tablename__ = 'utilisateurs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')  # 'admin' ou 'user'
    actif = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Utilisateur(username='{self.username}', role='{self.role}')>"
