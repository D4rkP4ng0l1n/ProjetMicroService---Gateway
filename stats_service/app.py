from flask import Flask, jsonify
from flasgger import Swagger
import random

app = Flask(__name__)
swagger = Swagger(app)

def generate_channels():
    channels = ["general", "random", "help", "announcements", "off-topic"]
    return {channel: random.randint(10, 1000) for channel in channels}

def generate_hourly_activity():
    hours = [f"{h:02d}:00" for h in range(24)]
    return {hour: random.randint(0, 500) for hour in hours}

def generate_messages_per_user():
    users = ["user1", "user2", "user3", "user4", "user5"]
    return {user: random.randint(5, 200) for user in users}

def generate_top_reacted_messages():
    messages = [
        {"id": 1, "content": "Bonjour tout le monde!", "reactions": random.randint(10, 100)},
        {"id": 2, "content": "Quoi de neuf?", "reactions": random.randint(10, 100)},
        {"id": 3, "content": "Avez-vous vu ça?", "reactions": random.randint(10, 100)},
        {"id": 4, "content": "Merci pour votre aide!", "reactions": random.randint(10, 100)},
        {"id": 5, "content": "Bonne journée!", "reactions": random.randint(10, 100)},
    ]
    return sorted(messages, key=lambda x: x["reactions"], reverse=True)

@app.route("/stats", methods=["GET"])
def get_stats():
    """
    Statistiques globales
    ---
    responses:
      200:
        description: Statistiques générées
        examples:
          application/json: {
            "visitors": 1234,
            "bounce_rate": 45.6,
            "conversion_rate": 3.2,
            "average_session_time": 120.5
          }
    """
    stats = {
        "visitors": random.randint(100, 10000),
        "bounce_rate": round(random.uniform(20.0, 80.0), 2),
        "conversion_rate": round(random.uniform(1.0, 10.0), 2),
        "average_session_time": round(random.uniform(30.0, 300.0), 1)
    }
    return jsonify(stats)

@app.route("/stats/active-channels", methods=["GET"])
def get_active_channels():
    """
    Activité par canal
    ---
    responses:
      200:
        description: Nombre de messages par canal
    """
    return jsonify(generate_channels())

@app.route("/stats/hourly-activity", methods=["GET"])
def get_hourly_activity():
    """
    Activité horaire
    ---
    responses:
      200:
        description: Nombre de messages par heure
    """
    return jsonify(generate_hourly_activity())

@app.route("/stats/messages-per-user", methods=["GET"])
def get_messages_per_user():
    """
    Messages par utilisateur
    ---
    responses:
      200:
        description: Nombre de messages par utilisateur
    """
    return jsonify(generate_messages_per_user())

@app.route("/stats/top-reacted-messages", methods=["GET"])
def get_top_reacted_messages():
    """
    Messages les plus réactifs
    ---
    responses:
      200:
        description: Liste triée des messages avec le plus de réactions
    """
    return jsonify(generate_top_reacted_messages())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
