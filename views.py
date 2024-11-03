from flask import Flask, render_template, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from forms import *
from models import *
import os
import dataaccess as da
import pickle

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
        user = da.auth(form.username.data, form.password.data)
        if user is None:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("login"))
        session["username"] = user.username
        # ここにカートとかが入るかもしれない
        return redirect(url_for("index"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/addlearn", methods=["GET", "POST"])
def addlearn():
    if "username" not in session:
        flash("You need to login first.", "warning")
        return redirect(url_for("login"))
    form = AddLearnForm()
    if form.validate_on_submit():
        learn = Learn()
        form.copy_to(learn)
        user = da.search_user_by_username(session["username"])
        learn.user_id = user.id
        da.addlearn(learn)
        flash("Learning log has been added.", "info")
        return redirect(url_for("addlearn"))
    user = da.search_user_by_username(session["username"])
    learn_list = da.search_learns_by_user(user.id)
    return render_template("addlearn.html", form=form, learn_list=learn_list)

@app.route("/searchlearn", methods=["GET", "POST"])
def search_learn():
    if "username" not in session:
        flash("You need to login first.", "warning")
        return redirect(url_for("login"))
    form = SearchLearnForm()
    if form.validate_on_submit():
        user = da.search_user_by_username(session["username"])
        learn_list = da.search_learn_by_field(user.id, form.itemname.data)
        session["learn_list"] = pickle.dumps(learn_list)
        return redirect(url_for("searchlearn"))
    if "learn_list" in session:
        learn_list = pickle.loads(session["learn_list"])
        session.pop("learn_list", None)
    else:
        user = da.search_user_by_username(session["username"])
        learn_list = da.search_learn_by_field(user.id, "")
    return render_template("searchlearn.html", form=form, learn_list=learn_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
