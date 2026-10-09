from flask import Blueprint, flash, redirect, render_template, request, session, url_for

import database
from seguranca import exigir_login, usuario_logado


leituras_bp = Blueprint("leituras", __name__)


@leituras_bp.route("/leituras")
def index():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    usuario_id = usuario_logado()
    leituras = database.listar_leituras(usuario_id)
    return render_template("leituras.html", leituras=leituras, usuario_id=usuario_id, usuario_nome=session.get("usuario_nome"))


@leituras_bp.route("/leituras/nova", methods=["GET", "POST"])
def nova_leitura():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        paginas = int(request.form["paginas"])
        database.criar_leitura(usuario_logado(), titulo, autor, paginas)
        flash("Leitura cadastrada.")
        return redirect(url_for("leituras.index"))

    return render_template("nova_leitura.html")


@leituras_bp.route("/leituras/<int:leitura_id>/editar", methods=["GET", "POST"])
def editar_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    usuario_id = usuario_logado()
    leitura = database.buscar_leitura(leitura_id, usuario_id)
    if leitura is None:
        return "Leitura não encontrada", 404

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        paginas = int(request.form["paginas"])
        database.atualizar_leitura(leitura_id, usuario_id, titulo, autor, paginas)
        flash("Leitura atualizada.")
        return redirect(url_for("leituras.index"))

    return render_template("editar_leitura.html", leitura=leitura)


@leituras_bp.post("/leituras/<int:leitura_id>/concluir")
def concluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    database.alternar_concluida(leitura_id, usuario_logado())
    flash("Status da leitura atualizado.")
    return redirect(url_for("leituras.index"))


@leituras_bp.post("/leituras/<int:leitura_id>/excluir")
def excluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    database.excluir_leitura(leitura_id, usuario_logado())
    flash("Leitura excluída.")
    return redirect(url_for("leituras.index"))
