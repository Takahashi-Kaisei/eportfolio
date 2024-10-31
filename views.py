from flask import Flask, render_template, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from forms import *
from models import *
import os
import dataaccess as da

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
    if form.validate_on_submit():
        if form.password.data != "password":
            user = da.auth(form.username.data, form.password.data)
        if user is None:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("login"))
        return redirect(url_for("index"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None) # セッションからusernameを削除
    session.clear() # セッションをクリア，すべてのセッション情報を削除
    flash("You have been logged out.", "info") #ここのinfoはBootstrapのalert-info
    return redirect(url_for("index")) # ログアウト後はindex.htmlにリダイレクト


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
