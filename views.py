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
        if form.password.data != "password":
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
    session.pop("username", None) # セッションからusernameを削除
    session.clear() # セッションをクリア，すべてのセッション情報を削除
    flash("You have been logged out.", "info") #ここのinfoはBootstrapのalert-info
    return redirect(url_for("index")) # ログアウト後はindex.htmlにリダイレクト

@app.route("/addlearn", methods=["GET", "POST"])
def addlearn():
    if "username" not in session:
        flash("You need to login first.", "warning")
        return redirect(url_for("login"))

    form = AddLearnForm()
    if form.validate_on_submit():
        # 現在ログインしているユーザーを検索
        user = da.search_user_by_username(session["username"])
        if user is None:
            flash("User not found", "danger")
            return redirect(url_for("index"))

        # フォームからのデータを取得
        learn_field = form.learn_field.data
        learn_date = form.learn_date.data
        learn_content = form.learn_content.data

        # データベースに保存
        da.add_learn(user.id, learn_field, learn_date, learn_content)

        flash("Learning content added successfully", "success")
        return redirect(url_for("index"))

    return render_template("addlearn.html", form=form)

@app.route("/searchlearn", methods=["GET", "POST"])
def search_learn():
    if "username" not in session:
        flash("You need to login first.", "warning")
        return redirect(url_for("login"))
    form = SearchLearnForm()
    learn_list = []
    if form.validate_on_submit():
        user = da.search_user_by_username(session["username"])
        learn_list = da.search_learn_by_field(user.id, form.itemname.data)
        session["learn_list"] = pickle.dumps(learn_list)
        return redirect(url_for("search_learn"))
    if "learn_list" in session:
        learn_list = pickle.loads(session["learn_list"])
        session.pop("learn_list", None)
    return render_template("searchlearn.html", form=form, learn_list=learn_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
