from flask import Flask, render_template, session, request, redirect, url_for, flash
from models.usuario import Usuario
from models.servico import Servico
from models.servico_categoria import ServicoCategoria
from models.usuario_tipo import UsuarioTipo
from models.veiculo_tipo import VeiculoTipo
from models.agendamento_servico import AgendamentoServico
from config import FLASK
from datetime import datetime, date
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)

# Chave secreta para proteger a sessão do flask (session)
app.secret_key = FLASK["secret_key"]

@app.route("/")
def home():
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
        if (usuario):
            if (usuario.validar_senha(senha)):
                session["id"] = usuario.id
                isAdmin = UsuarioTipo.is_admin(usuario.tipo_id)
                isFuncionario = UsuarioTipo.is_funcionario(usuario.tipo_id)
                session["admin"] = isAdmin
                session["funcionario"] = isFuncionario
                return redirect(url_for("home"))
            else:
                flash("A senha está incorreta", "error")
        else:
            flash("Usuário não cadastrado", "error")

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
        usuario_senha = request.form["senha"]
        usuario_colaborador = request.form["colaborador"]
        tipo_id = 1
        if usuario_colaborador:
            tipo_id = 2

        usuario = Usuario(tipo_id=tipo_id, nome=usuario_nome, email=usuario_email, senha=usuario_senha)
        usuario.inserir()
        return redirect(url_for("login"))

    return render_template("cadastro_cliente.html")

@app.route("/perfil")
def perfil():
    if (not "id" in session):
        return redirect(url_for("login"))

    usuario = Usuario.buscar(session["id"])
    return render_template("perfil.html", usuario=usuario)

@app.route("/veiculos")
def meus_veiculos():
    if (not "id" in session):
        return redirect(url_for("home"))

    return render_template("meus_veiculos.html", veiculos=None)

@app.route("/cadastrar_servico", methods=["GET","POST"])
def cadastrar_servico():
    if (not "id" in session):
        return redirect(url_for("login"))
    
    if (session["admin"] == False) and (session["funcionario"] == False):
        return redirect(url_for("home"))
    
    if (request.method == "POST"):
        servico_nome = request.form["nome"]
        servico_preco = request.form["preco"]
        servico_categoria_id = request.form["categoria"]
        servico_descricao = request.form["descricao"]
        servico_duracao_estimada = request.form["duracao"]
        servico = Servico(nome=servico_nome, preco=servico_preco, categoria_id=servico_categoria_id, descricao=servico_descricao, duracao_estimada=servico_duracao_estimada)
        servico.inserir()
        return redirect(url_for("home"))

    servico_categorias = ServicoCategoria.buscar_todas_categorias()
    return render_template("cadastro_servico.html", servico_categorias=servico_categorias)

@app.route("/agendar_servico", methods=["GET","POST"])
def agendar_servico(): 
    if (not "id" in session):
        return redirect(url_for("login"))
    
    if (request.method == "POST"):
        veiculo_tipo_id = request.form["veiculo_tipo"]
        servico_id = request.form["servico"]
        cliente_id = session["id"]
        data = request.form["data"]
        hora = request.form["hora"]
        data_hora_agendamento = datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
        agendamento_servico = AgendamentoServico(veiculo_tipo_id=veiculo_tipo_id, cliente_id=cliente_id, servico_id=servico_id, data_hora_agendamento=data_hora_agendamento, status_id=1)
        agendamento_servico.inserir()
        return redirect(url_for("home"))

    servicos = Servico.buscar_todos_servicos()
    veiculo_tipos = VeiculoTipo.buscar_todos_tipos()
    return render_template("agendar_servico.html", servicos=servicos, veiculo_tipos=veiculo_tipos)

@app.route("/servicos_agendados")
def servicos_agendados():
    if (not "id" in session):
        return redirect(url_for("login"))
    
    data_filtro = request.args.get("data")
    
    if (session["admin"] == False) and (session["funcionario"] == False):
        servicos_agendados = AgendamentoServico.buscar_servicos_agendados_usuario(session["id"], data_filtro)
        return render_template("servicos_agendados.html", servicos_agendados=servicos_agendados)

    servicos_agendados = AgendamentoServico.buscar_todos_servicos_agendados(data_filtro)
    return render_template("servicos_agendados.html", servicos_agendados=servicos_agendados)

@app.route("/agendamento/<int:id>")
def detalhes_agendamento(id):
    if (not "id" in session):
        return redirect(url_for("login"))

    agendamento = AgendamentoServico.buscar(id)
    return render_template("detalhes_agendamento.html",agendamento=agendamento)

@app.route("/cancelar_agendamento/<int:agendamento_id>", methods=["POST"])
def cancelar_agendamento(agendamento_id):
    if ("id" in session):
        AgendamentoServico.cancelar_agendamento(agendamento_id)
        return redirect(url_for("servicos_agendados"))
    
@app.route("/iniciar_agendamento/<int:agendamento_id>", methods=["POST"])
def iniciar_agendamento(agendamento_id):
    if ("id" in session):
        AgendamentoServico.iniciar_agendamento(agendamento_id, session["id"])
        return redirect(url_for("servicos_agendados"))
    
@app.route("/finalizar_agendamento/<int:agendamento_id>", methods=["POST"])
def finalizar_agendamento(agendamento_id):
    if ("id" in session):
        AgendamentoServico.finalizar_agendamento(agendamento_id)
        return redirect(url_for("servicos_agendados"))
    
@app.route("/relatorio")
def relatorio():
    if (not "id" in session):
        return redirect(url_for("login"))
    
    if (not session["admin"] and not session["funcionario"]):
        return redirect(url_for("home"))
    
    data_hoje = date.today()
    servicos_realizados = AgendamentoServico.buscar_todos_servicos_agendados(data_hoje, 2)
    
    return render_template("relatorio.html", data_hoje=data_hoje, servicos_realizados=servicos_realizados)

@app.route("/dashboard")
def dashboard():
    if (not "id" in session):
        return redirect(url_for("login"))
    
    if (not session["admin"] and not session["funcionario"]):
        return redirect(url_for("home"))

    df = AgendamentoServico.total_servicos_por_tipo_veiculo()

    fig = go.Figure(data=[
        go.Bar(x=df["veiculo_tipo_nome"], y=df["quantidade"], marker_color='steelblue')
    ])
    fig.update_layout(title="Agendamentos por Tipo de Veículo")

    grafico_html = pyo.plot(fig, output_type="div")
    return render_template("dashboard_veiculos.html", grafico_html=grafico_html)

@app.route("/logout")
def logout():
    # Remove a sessão do usuário e redireciona para o login
    session.clear()
    return redirect(url_for("login"))

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/avaliacoes")
def avaliacoes():
    return render_template("avaliacoes.html")

@app.route("/servicos")
def servicos():
    return render_template("servicos.html")

@app.route("/agendamento")
def agendamento():
    return render_template("agendamento.html")

if (__name__ == "__main__"):
    app.run(debug=True)