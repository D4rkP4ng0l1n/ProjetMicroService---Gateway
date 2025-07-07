---
titre: Architecture micro-service
sous-titre: Point tech - Pipenv
auteur: Philippe \textsc{Roussille}
theme: Warsaw
lang: fr-FR
section-titles: false
fontsize: 10pt
couleur-type-1: true
rendu-type: papier
rendu-logo: 3il
---

# Compétence outil : gérer ses dépendances avec `pipenv`

Dans le TP, chaque micro-service Python a ses propres dépendances (Flask, requests, PyJWT, etc).
Pour les gérer proprement, **on utilise `pipenv`** : un outil moderne qui combine un environnement virtuel + un fichier de dépendances.

## Pourquoi utiliser `pipenv` ?

- Crée automatiquement un **environnement virtuel** isolé
- Gère deux fichiers : `Pipfile` (dépendances) et `Pipfile.lock` (versions gelées)
- Plus propre que `pip install` global

## Commandes utiles

### Créer un projet et installer une lib (ex: Flask)

```bash
pipenv install flask
```

Cela crée :

- `Pipfile` → liste des paquets
- `Pipfile.lock` → versions exactes

### Lancer un shell dans l'environnement

```bash
pipenv shell
```

### Installer un autre paquet (ex: PyJWT)

```bash
pipenv install pyjwt
```

### Lister les paquets

```bash
pipenv graph
```

## Et pour Docker ?

Les conteneurs Python ont besoin d'un fichier `requirements.txt`. Voici comment le générer depuis `pipenv` :

```bash
pipenv lock --requirements > requirements.txt
```

Cela crée un fichier standard `requirements.txt` compatible avec tous les `Dockerfile` Python.

## Exemple de `Dockerfile` avec pipenv converti

```Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

# Installer les dépendances via requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

# Bonnes pratiques

- Ne versionnez pas `.venv/` → ajoutez-le à `.gitignore`
- Pensez à régénérer `requirements.txt` après chaque changement
- Vous pouvez aussi ajouter `pipenv install --dev pytest` pour les tests
