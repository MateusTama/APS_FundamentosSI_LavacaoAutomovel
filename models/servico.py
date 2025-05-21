from db import get_connection

class Servico:
    def __init__(self, id=None, nome=None, categoria_id=None, descricao=None, preco=None, duracao_estimada=None):
        self.id = id
        self.nome = nome
        self.categoria_id = categoria_id
        self.descricao = descricao
        self.preco = preco
        self.duracao_estimada = duracao_estimada

    def inserir(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO servico
            (servico_nome, servico_categoria_id, servico_descricao, servico_preco, servico_duracao_estimada)
            VALUES
            (%s, %s, %s, %s, %s)            
        """, (self.nome, self.categoria_id, self.descricao, self.preco, self.duracao_estimada))

        conn.commit()
        cursor.close()
        conn.close()

    def buscar_todos_servicos():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT servico_id, servico_nome, servico_categoria_id, servico_descricao, servico_preco, servico_duracao_estimada
            FROM servico
        """)

        resultados = cursor.fetchall()
        servicos = []
        for servico in resultados:
            servicos.append(Servico(servico[0], servico[1], servico[2], servico[3], servico[4], servico[5]))

        conn.commit()
        cursor.close()
        conn.close()

        return servicos
