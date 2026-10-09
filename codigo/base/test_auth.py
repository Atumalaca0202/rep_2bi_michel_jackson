import unittest
import uuid

from flask import Flask
from werkzeug.security import check_password_hash

import database
from auth import auth_bp
from leituras import leituras_bp


class AuthFlowTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "reposição"
        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(leituras_bp)
        database.criar_banco()

    def criar(self):
        email = f"usuario_{uuid.uuid4().hex}@teste.com"

        response = self.app.test_client().post(
            "/registro",
            data={"nome": "Maria", "email": email, "senha": "123"},
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

        usuario = database.buscar_usuario_por_email(email)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nome, "Maria")
        self.assertTrue(check_password_hash(usuario.senha_hash, "123"))

    def apagar_dados(self):
        email = f"usuario_{uuid.uuid4().hex}@teste.com"
        usuario = database.criar_usuario("Maria", email, "hash_qualquer")

        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess["usuario_id"] = usuario.id

            response = client.get("/logout", follow_redirects=False)

            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertNotIn("usuario_id", sess)


if __name__ == "__main__":
    unittest.main()
