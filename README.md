# Gestion de Stock - Application Python

## Description
Application de gestion de stock avec interface console interactive.  
Base de données PostgreSQL avec Docker Compose.

---

## Architecture

```
BDD/
├── docker-compose.yml      # Configuration Docker (PostgreSQL + pgAdmin)
├── init.sql                # Script d'initialisation de la BDD
├── requirements.txt        # Dépendances Python
├── .env                    # Variables d'environnement
└── python/
    ├── connexion.py        # Connexion à la BDD (psycopg2)
    ├── categorie.py        # CRUD catégories
    ├── fournisseur.py      # CRUD fournisseurs
    ├── produit.py          # CRUD produits
    ├── mouvement.py        # CRUD mouvements de stock
    ├── utilisateur.py      # CRUD utilisateurs + authentification
    └── main.py             # Application principale (menu interactif)
```

---

## Prérequis

- **Docker** et **Docker Compose**
- **Python 3.8+**
- **pip**

---

## Installation et Lancement

### 1. Démarrer la base de données

```bash
# Dans le dossier BDD/
docker-compose up -d
```

Cela démarre :
- **PostgreSQL** sur le port `5432`
- **pgAdmin** sur le port `8080` (interface web)

### 2. Vérifier que la BDD est prête

```bash
docker-compose logs db
```

Attendre le message "database system is ready to accept connections".

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
cd python
python main.py
```

---

## Connexion par défaut

| Utilisateur | Mot de passe | Rôle  |
|-------------|--------------|-------|
| admin       | admin123     | admin |

---

## Commandes Docker utiles

```bash
# Démarrer les conteneurs
docker-compose up -d

# Arrêter les conteneurs
docker-compose down

# Voir les logs
docker-compose logs -f

# Réinitialiser la BDD (supprimer les données)
docker-compose down -v
docker-compose up -d

# Accéder au shell PostgreSQL
docker exec -it stock_management_db psql -U stock_user -d gestion_stock
```

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
- ✅ Catégories : Créer, Lire, Modifier, Supprimer
- ✅ Fournisseurs : Créer, Lire, Modifier, Supprimer
- ✅ Produits : Créer, Lire, Modifier, Supprimer, Rechercher
- ✅ Mouvements : Entrée stock, Sortie stock, Historique
- ✅ Utilisateurs : Créer, Lister, Modifier MDP, Désactiver

### Sécurité
- ✅ Authentification par mot de passe hashé (SHA256)
- ✅ Rôles utilisateur (admin / user)
- ✅ Menu admin réservé aux administrateurs

### Alertes
- ✅ Détection automatique des produits sous le seuil d'alerte

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
