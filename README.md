# CanaDuck IRC – Client & Stats (Groupe 4)

---

# 👥 Membres du groupe

| Nom     | Rôle                          |
| ------- | ----------------------------- |
| Florian | Coordination                  |
| Younes  | Dev stats                     |
| Clément | Dev client + documentation    |


---

# 🔧 Technologies utilisées
- Python 3.11
- Flask
- Requests
- Docker / Docker Compose
- Traefik
- MySQL (via SQLAlchemy pour les services internes)

---

# 📁 Services développés par notre groupe
stats-service : service interne qui agrège des données statistiques sur les messages, utilisateurs et canaux.
client : Une interface permettant d'accéder aux différents micro-service

---

# 📊 Routes disponibles dans le `stats-service`

| Méthode | URL                         | Description                           |
| ------- | --------------------------- | ------------------------------------- |
| GET     | /stats/active-channels      | Liste des canaux les plus actifs      |
| GET     | /stats/hourly-activity      | Activité horaire (volume de messages) |
| GET     | /stats/messages-per-user    | Nombre total de messages par user     |
| GET     | /stats/top-reacted-messages | Messages les plus réactés             |

---

# 🚀 Lancer le projet (mode local avec Docker)

### 🔁 Prérequis

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


### 📦 Clonage du dépôt
```bash
git clone https://github.com/ton-utilisateur/canaduck-final.git
cd canaduck-final
```

### 🐳 Lancement avec Docker Compose
```bash
docker compose up --build
```
💡 Le reverse proxy Traefik expose tous les services via http://localhost:8081.

### 🐍 Utiliser client.py
