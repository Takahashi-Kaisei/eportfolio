from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from forms import *
import os

app = Flask(__name__)
bs = Bootstrap(app)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["WTF_CSRF_SECRET_KEY"] = os.urandom(32)
app.config["WTF_CSRF_ENABLED"] = True
csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
