---
titre: Architecture micro-service
sous-titre: Point cours - le JWT
auteur: Philippe \textsc{Roussille}
theme: Warsaw
lang: fr-FR
section-titles: false
fontsize: 10pt
couleur-type-1: true
rendu-type: papier
rendu-logo: 3il
---

# JWT par l'exemple

Un **JWT (JSON Web Token)** est une sorte de **badge numérique signé** qu'un utilisateur obtient après s'être connecté.
Il contient des informations comme son pseudo, ses rôles, sa date d'expiration… et il permet de **prouver son identité** auprès des autres services.

## Pourquoi utiliser JWT ?

- L'utilisateur s'authentifie **une seule fois** (`/login`)
- Le token est **signé** par le `user-service`, donc infalsifiable
- Les autres services peuvent le **vérifier localement**, sans avoir à redemander

## Exemple de contenu d'un JWT

```json
{
  "user": "roger",
  "roles": ["admin"],
  "exp": 1718544300
}
```

## Dans la requête HTTP

Le client ***doit*** envoyer le JWT dans l'en-tête de ***chaque*** requête :

```http
Authorization: Bearer <le_token>
```

# Exemple complet avec Flask et PyJWT

## Créez un fichier Python

```python
import jwt
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = "une_clé_secrète_partagée"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    pseudo = data.get("pseudo")
    if not pseudo:
        return jsonify({"error": "pseudo manquant"}), 400

    payload = {
        "user": pseudo,
        "roles": ["user"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

@app.route("/protected")
def protected():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Token manquant"}), 401

    token = auth[7:]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"status": "ok", "user": decoded["user"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expiré"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalide"}), 401

if __name__ == "__main__":
    app.run(port=5000)
```

## Installez les dépendances

Dans un terminal :

```bash
pip install flask pyjwt
```

## Lancez le serveur Flask

```bash
python votre_fichier_flask.py
```

## Testez l'authentification avec `curl`

### Obtenir un token JWT

```bash
curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"pseudo": "roger"}'
```

Résultat :

```json
{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOi..." }
```

### Accéder à une route protégée

```bash
curl http://localhost:5000/protected \
     -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

Résultat :

```json
{ "status": "ok", "user": "roger" }
```


# Que retenir

- Le JWT **remplace une session**
- Il est **vérifiable localement** dans un micro-service
- Il expire : on peut contrôler la durée de validité
- On ne stocke **jamais** le token côté serveur : c'est le client qui le garde
