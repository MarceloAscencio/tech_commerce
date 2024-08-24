from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for
from flask_login import (current_user, LoginManager,
                         login_user, logout_user, login_required)
import hashlib

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuarioframe:1234@localhost:3306/banco_dados'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://marceloascenciof:11031994marcelo@marceloascenciofilho.mysql.pythonanywhere-services.com:3306/marceloascenciof$banco_dados'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://marceloascenciof:11031994marcelo@marceloascenciofilho.mysql.pythonanywhere-services.com:3306/marceloascenciof$banco_dados'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = 'marcelo1103'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('codigo_usuario', db.Integer, primary_key=True)
    nome = db.Column('nome_usuario', db.String(250))
    cpf = db.Column('cpf_usuario', db.String(15))
    nasc = db.Column('nasc_usuario', db.Integer)
    email = db.Column('email_usuario', db.String(250))
    endereco = db.Column('endereco_usuario', db.String(250))
    senha = db.Column('senha_usuario', db.String(250))
    
    def __init__(self, nome, cpf, nasc, email, endereco, senha):
        self.nome = nome
        self.cpf = cpf
        self.nasc = nasc
        self.email = email
        self.endereco = endereco
        self.senha = senha

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)    
        
class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('codigo_categoria', db.Integer, primary_key=True)
    nomecat = db.Column('nome_categoria', db.String(250))
    descricat = db.Column('descricao_categoria', db.String(250))
    datacria = db.Column('data_categoria',db.String(250))

    def __init__(self,nomecat,descricat,datacria):
        self.nomecat = nomecat
        self.descricat = descricat
        self.datacria = datacria

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('codigo_anuncio', db.Integer, primary_key=True)
    nome_anuncio = db.Column('nome_anuncio',db.String(250))
    descri_anuncio = db.Column('descri_anuncio',db.String(250))
    valor = db.Column('valor_anuncio',db.String(250))
    localiza = db.Column('localizacao',db.String(250))

    def __init__(self, nome_anuncio,descri_anuncio,valor,localiza):
        self.nome_anuncio = nome_anuncio
        self.descri_anuncio = descri_anuncio
        self.valor = valor
        self.localiza = localiza

class Compras(db.Model):
    __tablename__ = "Compras"
    id = db.Column('condigo_compra', db.Integer, primary_key=True)
    valor_compra = db.Column('valor_compra', db.String(250))
    metodo_pagamento = db.Column('metodo_pagamento', db.String(250))
    codigo_usuario = db.Column('codigo_usuario', db.Integer, db.ForeignKey('usuario.codigo_usuario'), nullable=False)
    codigo_anuncio = db.Column('codigo_anuncio', db.Integer, db.ForeignKey('anuncio.codigo_anuncio'), nullable=False)

    def __init__(self,valor_compra,data_compra,metodo_pagamento, codigo_usuario, codigo_anuncio):
        self.valor_compra = valor_compra
        self.metodo_pagamento = metodo_pagamento
        self.codigo_usuario = codigo_usuario
        self.codigo_anuncio = codigo_anuncio


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('iemail')
        senha = request.form.get('isenha')

        user = Usuario.query.filter_by(email = email, senha = senha).first()

        if user:
            login_user(user)
            return redirect (url_for('index'))
        else:
            return redirect (url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/usuario")
def usuario():
    return render_template("usuarios.html", usuarios = Usuario.query.all()) 

@app.route("/caduser", methods=["POST"])
def caduser():
    hash = hashlib.sha512(str(request.form.get('isenha')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('inome'),request.form.get('icpf'),request.form.get('inasc'),request.form.get('iemail'),request.form.get('iend'),hash)
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscausuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=["GET","POST"])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('inome')
        usuario.cpf = request.form.get('icpf')
        usuario.nasc = request.form.get('inasc')
        usuario.email = request.form.get('iemail')
        usuario.senha = request.form.get('isenha')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))
    return render_template('editarusuario.html', usuario = usuario)

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
     usuario = Usuario.query.get(id)
     db.session.delete(usuario)
     db.session.commit()
     return redirect(url_for('usuario'))


@app.route("/categoria")
def categoria():
    return render_template("categoria.html", categorias = Categoria.query.all())

@app.route("/cadcategoria", methods=["POST"])
def cadastrarcategoria():
    categoria = Categoria(request.form.get('inomecat'), request.form.get('idescricao'), request.form.get('idatacria'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>", methods=["GET", "POST"])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nomecat = request.form.get('inomecat')
        categoria.descricat = request.form.get('idescricao')
        categoria.datacria = request.form.get('idatacria')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('editarcategoria.html', categoria = categoria)

@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
     categoria = Categoria.query.get(id)
     db.session.delete(categoria)
     db.session.commit()
     return redirect(url_for('categoria'))

@app.route("/anuncios")
@login_required
def anuncios():
    return render_template("anuncios.html", anuncios = Anuncio.query.all())

@app.route("/cadanuncio", methods=["POST"])
def cadastraranuncio():
    anuncio = Anuncio(request.form.get('inomeanuncio'), request.form.get('idescricaoanuncio'), request.form.get('ivaloranuncio'), request.form.get('ilocalizacaoanuncio'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncios'))

@app.route("/anuncios/editar/<int:id>", methods=["GET", "POST"])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome_anuncio = request.form.get('inomeanuncio')
        anuncio.descri_anuncio = request.form.get('idescricaoanuncio')
        anuncio.valor = request.form.get('ivaloranuncio')
        anuncio.localiza = request.form.get('ilocalizacaoanuncio')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncios'))
    return render_template('editaranuncio.html', anuncio = anuncio)

@app.route("/anuncios/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncios'))


@app.route("/compras")
def compras():
    return render_template("compras.html", compras = Compras.query.all())

@app.route("/cadcompras", methods=["POST"])
def cadastrar_compras():
    cadastroCompras = Compras(request.form.get('ivalor_produto'), request.form.get('idata_compra'), request.form.get('metodo_pagamento'), request.form.get('icodigo_produto'), current_user.id)
    db.session.add(cadastroCompras)
    db.session.commit()
    return redirect(url_for('compras'))

@app.route("/compras/editar/<int:id>", methods=["POST", "GET"])
def editarcompras(id):
    compra = Compras.query.get(id)
    if request.method == "POST":
        compra.valor_compra = request.form.get('ivalor_produto')
        compra.metodo_pagamento = request.form.get('metodo_pagamento')
        compra.valor_compra = request.form.get('ivalor_produto')
        db.session.add(compra)
        db.session.commit()
        return redirect(url_for('compras'))
    return render_template("editarcompras.html", compra = compra)

@app.route("/compras/deletar/<int:id>")
def deletarcompras(id):
    compra = Compras.query.get(id)
    db.session.delete(compra)
    db.session.commit()
    return redirect(url_for('compras'))

if __name__ == 'tech':
    with app.app_context():
        db.create_all()
    
