from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import Session, User
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 基本檢查
        if not username or not password:
            flash("請輸入帳號與密碼")
            return redirect(url_for("auth.register"))

        with Session() as session:
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                flash("此帳號已存在")
                return redirect(url_for("auth.register"))

            # 加密密碼
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)
            session.add(new_user)
            session.commit()

            login_user(new_user)  # 註冊完成直接登入
            return redirect(url_for("expense.expense"))

    return render_template("register.html")

@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "" or password == "":
            flash("請輸入帳號與密碼")
            return redirect(url_for("auth.login"))

        with Session() as session:
            user = session.query(User).filter_by(username = username).first()

            if not user or not check_password_hash(user.password_hash, password):
                flash("帳號或密碼錯誤")
                return redirect(url_for("auth.login"))

            login_user(user)
            return redirect(url_for("expense.expense"))
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("您已成功登出")
    return redirect(url_for("auth.login"))