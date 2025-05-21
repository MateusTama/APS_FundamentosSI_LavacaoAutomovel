from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id=None, tipo_id=None,nome=None, email=None, telefone=None, senha=None, data_hora_cadastro=None):
        self.id = id
        self.tipo_id = tipo_id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.data_hora_cadastro = data_hora_cadastro

    def inserir(self):
        conn = get_connection()
        cursor = conn.cursor()

        senha_hash = generate_password_hash(self.senha)

        cursor.execute("""
            INSERT INTO usuario
            (usuario_tipo_id, usuario_nome, usuario_email, usuario_telefone, usuario_senha)
            VALUES
            (%s, %s, %s, %s, %s)
        """, (self.tipo_id, self.nome, self.email, self.telefone, senha_hash))

        conn.commit()
        cursor.close()
        conn.close()

    def buscar(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT usuario_id, usuario_tipo_id, usuario_nome, usuario_email, usuario_telefone, usuario_senha, usuario_datahoracadastro 
            FROM usuario
            WHERE usuario_id = %s
        """, (id,))

        registro_usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if registro_usuario:
            # id = registro_usuario[0] igual ao parâmetro id 
            tipo_id = registro_usuario[1]
            nome = registro_usuario[2]
            email = registro_usuario[3] 
            telefone = registro_usuario[4]
            senha = registro_usuario[5]
            data_hora_cadastro = registro_usuario[6]
            return Usuario(id, tipo_id, nome, email, telefone, senha, data_hora_cadastro)
        
        return None

    def buscar_por_email(email):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT usuario_id, usuario_tipo_id, usuario_nome, usuario_email, usuario_telefone, usuario_senha, usuario_datahoracadastro 
            FROM usuario
            WHERE usuario_email = %s
        """, (email,))

        registro_usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if registro_usuario:
            id = registro_usuario[0]
            tipo_id = registro_usuario[1]
            nome = registro_usuario[2]
            # email = registro_usuario[3] igual ao parâmetro email
            telefone = registro_usuario[4]
            senha = registro_usuario[5]
            data_hora_cadastro = registro_usuario[6]
            return Usuario(id, tipo_id, nome, email, telefone, senha, data_hora_cadastro)
        
        return None
    
    def validar_senha(self, senha):
        return check_password_hash(self.senha, senha)