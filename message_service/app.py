from flask import Flask
app = Flask(__name__)

@app.route("/hey")
def index():
    return "Hello from the Hello app!"

@app.route("/hello/bro")
def hello() :
    return "Hello my petit frero !"

@app.route("/stats")
def stats() :
    return "Hello my petit frero (stats) !"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)