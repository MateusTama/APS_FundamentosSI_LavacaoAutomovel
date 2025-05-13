from db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servico (
            servico_id SERIAL PRIMARY KEY,
            servico_nome VARCHAR(100) NOT NULL,
            servico_preco DECIMAL(8,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario_tipo (
            usuario_tipo_id SMALLSERIAL PRIMARY KEY,
            usuario_tipo_perfil VARCHAR(40) NOT NULL UNIQUE 
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            usuario_id SERIAL PRIMARY KEY,
            usuario_tipo_id SMALLSERIAL NOT NULL,
            usuario_nome VARCHAR(100) NOT NULL,
            usuario_email VARCHAR(100) NOT NULL UNIQUE,
            usuario_telefone VARCHAR(14) NOT NULL UNIQUE,
            usuario_senha TEXT NOT NULL,
            usuario_datahoracadastro TIMESTAMP NOT NULL DEFAULT NOW(),
            FOREIGN KEY (usuario_tipo_id) REFERENCES usuario_tipo(usuario_tipo_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculo_tipo (
            veiculo_tipo_id SMALLSERIAL PRIMARY KEY,
            veiculo_tipo_nome VARCHAR(20)
        )
    """)

    cursor.execute("""
        CREATE TABLE veiculo (
            veiculo_id SERIAL PRIMARY KEY,
            proprietario_id INTEGER NOT NULL,
            veiculo_placa VARCHAR(10) NOT NULL UNIQUE,
            veiculo_modelo VARCHAR(100) NOT NULL,
            veiculo_marca VARCHAR(100) NOT NULL,
            veiculo_ano INTEGER,
            veiculo_cor VARCHAR(50),
            veiculo_ativo BOOLEAN DEFAULT TRUE,
            veiculo_tipo_id SMALLINT NOT NULL,
            veiculo_datahoracadastro TIMESTAMP NOT NULL DEFAULT NOW(),
            FOREIGN KEY (proprietario_id) REFERENCES usuario(usuario_id),
            FOREIGN KEY (veiculo_tipo_id) REFERENCES veiculo_tipo(veiculo_tipo_id)
        )
    """)
    
    cursor.execute("""
        INSERT INTO veiculo_tipo 
        (veiculo_tipo_nome) 
        VALUES (%s);
        
        INSERT INTO veiculo_tipo 
        (veiculo_tipo_nome) 
        VALUES (%s);
                   
        INSERT INTO veiculo_tipo 
        (veiculo_tipo_nome) 
        VALUES (%s);
    """, ("Moto", "Carro", "Caminhão"))

    cursor.execute("""
        INSERT INTO usuario_tipo 
        (usuario_tipo_perfil) 
        VALUES (%s);
        
        INSERT INTO usuario_tipo 
        (usuario_tipo_perfil) 
        VALUES (%s);
                   
        INSERT INTO usuario_tipo 
        (usuario_tipo_perfil) 
        VALUES (%s);
    """, ("Cliente", "Funcionario", "Administrador"))

    conn.commit()
    cursor.close()
    conn.close()

    print("As tabelas do banco de dados foram criadas com sucesso.")

if (__name__ == "__main__"):
    create_tables() 