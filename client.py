# -------------------- IMPORTS -------------------- #
from flask import Flask, request, jsonify
from flasgger import Swagger
import requests
# ------------------------------------------------- #

app = Flask(__name__)
swagger = Swagger(app)

# -------------------- METHODES GET -------------------- #

@app.route("/fullinfo?user=<string:user>&channel=<int:idchan>", methods=["GET"])
def get_full_info() :
    pass

@app.route("/stats", methods=["GET"])
def get_stats() :
    pass

@app.route("/hello/*", methods=["GET"])
def get_test_hello() :
    try :
        res = requests.get("http://localhost:8082", headers={"Host": "hello.localhost"})
        print("Réponse du service Hello :", res.text)
        
    except requests.exceptions.RequestException as e :
        print("Erreur lors de l'appel aux services :", e)

# -------------------- METHODES POST -------------------- #

@app.route("/register", methods=["POST"])
def register() :
    pass

@app.route("/login", methods=["POST"])
def login() :
    pass

# ------------------------------------------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)