from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuarioframe:1234@localhost:3306/banco_dados'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/usuario")
def usuario():
    return render_template("usuarios.html", usuarios = Usuario.query.all()) 

@app.route("/caduser", methods=["POST"])
def caduser():
    usuario = Usuario(request.form.get('inome'),request.form.get('icpf'),request.form.get('inasc'),request.form.get('iemail'),request.form.get('iend'),request.form.get('isenha'))
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
    return render_template("categoria.html")

@app.route("/cadcategoria", methods=["POST"])
def cadastrarcategoria():
    categoria = Categoria(request.form.get('inomecat'), request.form.get('idescricao'), request.form.get('idatacria'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/anuncios")
def anuncios():
    return render_template("anuncios.html")

@app.route("/compras")
def compras():
    return render_template("compras.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")


if __name__ == 'tech':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
