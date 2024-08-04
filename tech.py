from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/categoria")
def categoria():
    return render_template("categoria.html")

@app.route("/anuncios")
def anuncios():
    return render_template("anuncios.html")

@app.route("/compras")
def compras():
    return render_template("compras.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")
