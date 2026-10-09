from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        flash("Complete o cadastro usando database.py e generate_password_hash.")
        return redirect(url_for("auth.registro"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("Complete o login usando check_password_hash e session.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    flash("Complete o logout removendo os dados da session.")
    return redirect(url_for("auth.login"))
