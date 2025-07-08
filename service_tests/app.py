from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def index():
    return "Hello from the Hello app!"

@app.route("/hello/bro")
def hello() :
    return "Hello my petit frero !"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)