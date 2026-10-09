from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha nome, e-mail e senha.")
            return redirect(url_for("auth.registro"))

        if database.buscar_email(email):
            flash("Este e-mail já está cadastrado.")
            return redirect(url_for("auth.registro"))

        senha_hash = generate_password_hash(senha)
        database.criar_usuario(nome, email, senha_hash)
        flash("Cadastro realizado com sucesso. Faça login.")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        usuario = database.buscar_email(email)
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            flash("Login realizado com sucesso.")
            return redirect(url_for("leituras.index"))

        flash("E-mail ou senha inválidos.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado.")
    return redirect(url_for("auth.login"))
