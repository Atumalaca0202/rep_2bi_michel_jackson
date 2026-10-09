from flask import flash, redirect, session, url_for


def exigir_login():
    if "usuario_id" not in session:
        flash("Faça login para acessar esta página.")
        return redirect(url_for("auth.login"))
    return None


def usuario_logado():
    return session.get("usuario_id")
