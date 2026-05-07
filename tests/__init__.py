import os
from service import app
from service.models import db

# CONFIGURAR BANCO EM MEMÓRIA (ANTES DO init_app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)