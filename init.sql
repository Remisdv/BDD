-- ============================================
-- Script d'initialisation de la base de données
-- Gestion de Stock
-- ============================================

-- Extension pour les UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table des catégories de produits
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nom VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des fournisseurs
CREATE TABLE IF NOT EXISTS fournisseurs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nom VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telephone VARCHAR(20),
    adresse TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des produits
CREATE TABLE IF NOT EXISTS produits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reference VARCHAR(50) NOT NULL UNIQUE,
    nom VARCHAR(200) NOT NULL,
    description TEXT,
    prix_unitaire DECIMAL(10, 2) NOT NULL CHECK (prix_unitaire >= 0),
    quantite_stock INTEGER NOT NULL DEFAULT 0 CHECK (quantite_stock >= 0),
    seuil_alerte INTEGER DEFAULT 10 CHECK (seuil_alerte >= 0),
    categorie_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    fournisseur_id UUID REFERENCES fournisseurs(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des mouvements de stock (entrées/sorties)
CREATE TABLE IF NOT EXISTS mouvements_stock (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    produit_id UUID NOT NULL REFERENCES produits(id) ON DELETE CASCADE,
    type_mouvement VARCHAR(10) NOT NULL CHECK (type_mouvement IN ('ENTREE', 'SORTIE')),
    quantite INTEGER NOT NULL CHECK (quantite > 0),
    motif TEXT,
    date_mouvement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des utilisateurs (sécurité minimale)
CREATE TABLE IF NOT EXISTS utilisateurs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_produits_categorie ON produits(categorie_id);
CREATE INDEX IF NOT EXISTS idx_produits_fournisseur ON produits(fournisseur_id);
CREATE INDEX IF NOT EXISTS idx_produits_reference ON produits(reference);
CREATE INDEX IF NOT EXISTS idx_mouvements_produit ON mouvements_stock(produit_id);
CREATE INDEX IF NOT EXISTS idx_mouvements_date ON mouvements_stock(date_mouvement);

-- Fonction pour mettre à jour automatiquement updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers pour updated_at
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fournisseurs_updated_at BEFORE UPDATE ON fournisseurs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_produits_updated_at BEFORE UPDATE ON produits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_utilisateurs_updated_at BEFORE UPDATE ON utilisateurs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insertion de données de test
INSERT INTO categories (id, nom, description) VALUES
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Électronique', 'Produits électroniques et accessoires'),
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'Bureautique', 'Fournitures de bureau'),
    ('c3d4e5f6-a7b8-9012-cdef-123456789012', 'Informatique', 'Matériel informatique');

INSERT INTO fournisseurs (id, nom, email, telephone, adresse) VALUES
    ('d4e5f6a7-b8c9-0123-def0-234567890123', 'TechSupply', 'contact@techsupply.com', '0123456789', '123 Rue de la Tech, Paris'),
    ('e5f6a7b8-c9d0-1234-ef01-345678901234', 'BureauPro', 'info@bureaupro.com', '0987654321', '456 Avenue du Bureau, Lyon');

INSERT INTO produits (id, reference, nom, description, prix_unitaire, quantite_stock, seuil_alerte, categorie_id, fournisseur_id) VALUES
    ('f6a7b8c9-d0e1-2345-f012-456789012345', 'ELEC-001', 'Souris sans fil', 'Souris optique sans fil 2.4GHz', 25.99, 50, 10, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'd4e5f6a7-b8c9-0123-def0-234567890123'),
    ('a7b8c9d0-e1f2-3456-0123-567890123456', 'ELEC-002', 'Clavier mécanique', 'Clavier mécanique RGB', 89.99, 30, 5, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'd4e5f6a7-b8c9-0123-def0-234567890123'),
    ('b8c9d0e1-f2a3-4567-1234-678901234567', 'BURO-001', 'Stylo bleu', 'Lot de 10 stylos bleus', 5.99, 200, 50, 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'e5f6a7b8-c9d0-1234-ef01-345678901234'),
    ('c9d0e1f2-a3b4-5678-2345-789012345678', 'INFO-001', 'Câble HDMI 2m', 'Câble HDMI haute vitesse 2 mètres', 12.99, 100, 20, 'c3d4e5f6-a7b8-9012-cdef-123456789012', 'd4e5f6a7-b8c9-0123-def0-234567890123');

-- Utilisateur admin par défaut (mot de passe: admin123 - hashé avec SHA256)
-- Note: En production, changer ce mot de passe!
-- Hash SHA256 de "admin123" = 240be518fabd2724ddb6f04eeb9d5b0a
INSERT INTO utilisateurs (id, username, password_hash, role) VALUES
    ('00000000-0000-0000-0000-000000000001', 'admin', '240be518fabd2724ddb6f04eeb9d5b0aec142dce62670da4ad7b9d9b9f0b9de4', 'admin');
