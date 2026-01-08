# Projet de Gestion de Stock

Ce projet est une application en ligne de commande (CLI) pour la gestion de stocks, développée en Python. Elle utilise une base de données PostgreSQL, gérée avec Docker, pour assurer la persistance et la fiabilité des données.

## Description

L'application permet de suivre les produits, leurs catégories, les fournisseurs, ainsi que les mouvements de stock (entrées et sorties). Un système d'authentification simple basé sur les rôles (admin, utilisateur) est également inclus pour sécuriser l'accès aux différentes fonctionnalités.

## Fonctionnalités

- **Gestion des Produits**: CRUD complet (Créer, Lire, Mettre à jour, Supprimer) pour les produits.
- **Gestion des Catégories**: Organisez les produits par catégories.
- **Gestion des Fournisseurs**: Suivez les informations de vos fournisseurs.
- **Mouvements de Stock**: Enregistrez chaque entrée et sortie de produit pour un historique complet.
- **Authentification**: Système de connexion sécurisé avec des mots de passe hashés.
- **Interface en Ligne de Commande**: Menu interactif pour une utilisation simple et rapide.
- **Alertes de Stock**: Soyez notifié lorsque le stock d'un produit atteint un seuil critique.

## Technologies Utilisées

- **Langage**: Python 3
- **Base de données**: PostgreSQL
- **Conteneurisation**: Docker & Docker Compose
- **Bibliothèques Python**:
  - `psycopg2-binary`: Pour la connexion à la base de données PostgreSQL.
  - `bcrypt`: Pour le hachage des mots de passe.
  - `python-dotenv`: Pour la gestion des variables d'environnement.

## Architecture de la Base de Données

Le script `init.sql` initialise la structure suivante :

- `categories`: Stocke les catégories de produits.
- `fournisseurs`: Contient les informations sur les fournisseurs.
- `produits`: Table centrale contenant les détails des produits, avec des clés étrangères vers `categories` et `fournisseurs`.
- `mouvements_stock`: Enregistre toutes les transactions de stock pour chaque produit.
- `utilisateurs`: Gère les comptes utilisateurs et leurs rôles.

Des **index** sont créés pour optimiser les performances des requêtes et des **triggers** mettent à jour automatiquement les dates de modification.

## Démarrage Rapide

### Prérequis

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.8+](https://www.python.org/downloads/)

### Étapes d'installation

1.  **Clonez le dépôt** (si applicable) ou assurez-vous que tous les fichiers sont dans un même répertoire.

2.  **Créez un fichier `.env`** à la racine du projet en vous basant sur le modèle suivant pour configurer les accès à la base de données :

    ```env
    POSTGRES_DB=gestion_stock
    POSTGRES_USER=stock_user
    POSTGRES_PASSWORD=your_strong_password
    DB_PORT=5432
    ```

3.  **Démarrez le conteneur Docker** avec PostgreSQL :

    ```bash
    docker-compose up -d
    ```

    Cette commande va construire l'image, créer le volume pour la persistance des données et exécuter le script `init.sql`.

4.  **Installez les dépendances Python** :

    ```bash
    pip install -r requirements.txt
    ```

5.  **Lancez l'application** :

    ```bash
    python python/main.py
    ```

### Accès par défaut

Un utilisateur `admin` est créé par défaut pour le premier accès :
- **Nom d'utilisateur**: `admin`
- **Mot de passe**: `admin123`

## Commandes Docker Utiles

- **Démarrer les services en arrière-plan** :
  ```bash
  docker-compose up -d
  ```

- **Arrêter les services** :
  ```bash
  docker-compose down
  ```

- **Arrêter et supprimer les volumes (réinitialisation complète)** :
  ```bash
  docker-compose down -v
  ```

- **Consulter les logs du service de base de données** :
  ```bash
  docker-compose logs -f db
  ```

- **Se connecter à la base de données via `psql`** :
  ```bash
  docker exec -it stock_management_db psql -U stock_user -d gestion_stock
  ```

---
*Ce projet a été développé dans un but éducatif pour illustrer les concepts de base de données avec Python et Docker.*

---

## Accès pgAdmin (Interface Web)

- **URL** : http://localhost:8080
- **Email** : admin@admin.com
- **Password** : admin

Pour ajouter le serveur PostgreSQL dans pgAdmin :
- **Host** : db
- **Port** : 5432
- **Database** : gestion_stock
- **Username** : stock_user
- **Password** : stock_password

---

## Structure de la Base de Données

### Tables

| Table              | Description                          |
|--------------------|--------------------------------------|
| `categories`       | Catégories de produits               |
| `fournisseurs`     | Fournisseurs                         |
| `produits`         | Produits avec stock                  |
| `mouvements_stock` | Historique entrées/sorties           |
| `utilisateurs`     | Utilisateurs avec authentification   |

### Schéma relationnel

```
categories (1) ──────< (N) produits
fournisseurs (1) ────< (N) produits
produits (1) ────────< (N) mouvements_stock
```

---

## Fonctionnalités

### CRUD Complet
- Catégories : Créer, Lire, Modifier, Supprimer
- Fournisseurs : Créer, Lire, Modifier, Supprimer
- Produits : Créer, Lire, Modifier, Supprimer, Rechercher
- Mouvements : Entrée stock, Sortie stock, Historique
- Utilisateurs : Créer, Lister, Modifier MDP, Désactiver

### Sécurité
- Authentification par mot de passe hashé (SHA256)
- Rôles utilisateur (admin / user)
- Menu admin réservé aux administrateurs

### Alertes
- Détection automatique des produits sous le seuil d'alerte

---

## Configuration

### Variables d'environnement (.env)

```env
DATABASE_URL=postgresql://stock_user:stock_password@localhost:5432/gestion_stock
```

### Modifier les paramètres de connexion

Éditer le fichier `python/connexion.py` :

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'gestion_stock',
    'user': 'stock_user',
    'password': 'stock_password'
}
```

---

## Dépannage

### Erreur de connexion à la BDD

1. Vérifier que Docker est lancé
2. Vérifier que les conteneurs sont up : `docker-compose ps`
3. Attendre quelques secondes après le démarrage

### Réinitialiser complètement

```bash
docker-compose down -v
docker-compose up -d
```

---

## Technologies utilisées

- **Python 3** - Langage de programmation
- **psycopg2** - Driver PostgreSQL pour Python
- **PostgreSQL 16** - Base de données relationnelle
- **Docker Compose** - Orchestration des conteneurs
- **pgAdmin 4** - Interface d'administration web
- **tabulate** - Affichage des tableaux en console
