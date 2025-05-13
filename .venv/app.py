from flask import Flask, render_template, session, request, redirect, url_for
from models.usuario import Usuario
from models.servico import Servico
from config import FLASK

app = Flask(__name__)

# Chave secreta para proteger a sessão do flask (session)
app.secret_key = FLASK["secret_key"]

@app.route("/")
def home():
    if (not "id" in session):
        return redirect(url_for("login"))
    
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    # Se o usuário já estiver logado
    if ("id" in session):
        return redirect(url_for("home"))
    
    # Caso seja uma tentativa de login
    if (request.method == "POST"):
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.buscar_por_email(email)
        # Checa se a senha corresponde ao hash armazenado no banco de dados
        if (usuario) and (usuario.validar_senha(senha)):
            session["id"] = usuario.id
            return redirect(url_for("home"))

        # Senhas não correspondem
        # return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/cadastrar_cliente", methods=["GET","POST"])
def cadastrar_cliente():
    # Se já for um usuário logado
    if ("id" in session):
        return redirect(url_for("home"))
    
    if (request.method == "POST"):
        usuario_nome = request.form["nome"]
        usuario_email = request.form["email"]
        usuario_telefone = request.form["telefone"]
        usuario_senha = request.form["senha"]

        usuario = Usuario(tipo_id=1, nome=usuario_nome, email=usuario_email, telefone=usuario_telefone, senha=usuario_senha)
        usuario.inserir()
        return redirect(url_for("login"))

    return render_template("cadastro_cliente.html")

@app.route("/perfil")
def perfil():
    if (not "id" in session):
        return redirect(url_for("home"))

    usuario = Usuario.buscar(session["id"])
    return render_template("perfil.html", usuario=usuario)

@app.route("/veiculos")
def meus_veiculos():
    if (not "id" in session):
        return redirect(url_for("home"))

    return render_template("meus_veiculos.html", veiculos=None)

@app.route("/logout")
def logout():
    # Remove a sessão do usuário e redireciona para o login
    session.clear()
    return redirect(url_for("login"))

if (__name__ == "__main__"):
    app.run(debug=True)