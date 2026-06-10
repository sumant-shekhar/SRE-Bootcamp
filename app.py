from flask import Flask , render_template , request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "<h1 align='center'>Welcome to Home Page</h1>"

if __name__ == "__main__":
    app.run(port=4000, debug=True)
