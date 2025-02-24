# Google Sheet projet
Compte d'administration:
- login: admin_miage
- password: admin

# Page d'administration 
http://127.0.0.1:8000/admin/login/?next=/admin/

# Guide d'installation windows

*** Pré-requis: Python déjà installé ***
- Guide installation Python sous WIndows: https://docs.python.org/fr/3/using/windows.html

# Installation de Django-Framework
### Création d'un environnement virtuel
Ouvrir un terminal en ligne de commande (cmd): Touche "Win+r", taper "cmd", cd "My\path\to\this\crazy\project" ou de préference depuis un IDE de type VsCode (Onglet terminal).

Création de l'environement virtuel d'exexution:
```python
py -m venv env
```
Activation de l'environnement:
```python
env\Scripts\activate 
```
Si vous obtenez un problème d'autorisation, appliquer la procédure décrite dans le lien suivant: https://www.windows8facile.fr/powershell-execution-de-scripts-est-desactivee-activer/

### Installation de django
```python
py -m pip install Django
```
### Installation des dépendances du projet
```python
cd google_sheet
py -m pip install -r requirements.txt
```

### Migrer les modèles de donnée dans la base
```python
py manage.py migrate
py manage.py makemigrations
py manage.py migrate
```

# Executer l'application dans une console web
```python
py manage.py runserver
```
Une fenetre s'ouvre dans votre navigateur pour utiliser l'apapplication

# Commandes utiles
### Créer une fonctionnalité
```python
py manage.py startapp nomDeMaFonctionnalite
```


# Liens utiles pour utiliser Django
- https://www.w3schools.com/django/django_create_app.php

