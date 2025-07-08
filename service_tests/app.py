from flask import Flask, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Génère des données aléatoires pour les canaux
def generate_channels():
    channels = ["general", "random", "help", "announcements", "off-topic"]
    return {channel: random.randint(10, 1000) for channel in channels}

# Génère des données horaires aléatoires
def generate_hourly_activity():
    hours = [f"{h:02d}:00" for h in range(24)]
    return {hour: random.randint(0, 500) for hour in hours}

# Génère des données par utilisateur aléatoires
def generate_messages_per_user():
    users = ["user1", "user2", "user3", "user4", "user5"]
    return {user: random.randint(5, 200) for user in users}

# Génère des messages avec réactions aléatoires
def generate_top_reacted_messages():
    messages = [
        {"id": 1, "content": "Bonjour tout le monde!", "reactions": random.randint(10, 100)},
        {"id": 2, "content": "Quoi de neuf?", "reactions": random.randint(10, 100)},
        {"id": 3, "content": "Avez-vous vu ça?", "reactions": random.randint(10, 100)},
        {"id": 4, "content": "Merci pour votre aide!", "reactions": random.randint(10, 100)},
        {"id": 5, "content": "Bonne journée!", "reactions": random.randint(10, 100)},
    ]
    return sorted(messages, key=lambda x: x["reactions"], reverse=True)

@app.route("/", methods=["GET"])
def get_stats():
    stats = {
        "visitors": random.randint(100, 10000),
        "bounce_rate": round(random.uniform(20.0, 80.0), 2),
        "conversion_rate": round(random.uniform(1.0, 10.0), 2),
        "average_session_time": round(random.uniform(30.0, 300.0), 1)  # in seconds
    }
    return jsonify(stats)

@app.route("/active-channels", methods=["GET"])
def get_active_channels():
    channels = generate_channels()
    return jsonify(channels)

@app.route("/hourly-activity", methods=["GET"])
def get_hourly_activity():
    activity = generate_hourly_activity()
    return jsonify(activity)

@app.route("/messages-per-user", methods=["GET"])
def get_messages_per_user():
    messages = generate_messages_per_user()
    return jsonify(messages)

@app.route("/top-reacted-messages", methods=["GET"])
def get_top_reacted_messages():
    messages = generate_top_reacted_messages()
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
