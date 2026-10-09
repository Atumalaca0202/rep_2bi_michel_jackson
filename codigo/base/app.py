from flask import Flask, redirect, session, url_for

import database
from auth import auth_bp
from leituras import leituras_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = "reposição"


database.criar_banco()

app.register_blueprint(auth_bp)
app.register_blueprint(leituras_bp)


@app.route("/")
def index():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("leituras.index"))


if __name__ == "__main__":
    app.run(debug=True)
