# -------------------- IMPORTS -------------------- #
from flask import Flask, request, jsonify
from flasgger import Swagger
import requests
# ------------------------------------------------- #

app = Flask(__name__)
swagger = Swagger(app)

# ------------------------------------------------- #

BASE_URL = "http://localhost:8081"

def main():
    print("=== Test du microservice Hello ===\n")

    try:
        res1 = requests.get(f"{BASE_URL}/hello", headers={"Host": "service_test.localhost"})
        print(f"/hello -> {res1.text}")

        res2 = requests.get(f"{BASE_URL}/hello/bro", headers={"Host": "service_test.localhost"})
        print(f"/hello/bro -> {res2.text}")

    except requests.exceptions.ConnectionError:
        print("Erreur : impossible de se connecter au serveur.")
    except Exception as e:
        print("Erreur inattendue :", e)

if __name__ == "__main__":
    main()
    