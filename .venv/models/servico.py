from db import get_connection

class Servico:
    def __init__(self, id=None, nome=None, preco=None):
        self.id = id
        self.nome = nome
        self.preco = preco

    def inserir(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO servico
            (servico_nome, servico_preco)
            VALUES
            (%s, %s)            
        """, (self.nome, self.preco))

        conn.commit()
        cursor.close()
        conn.close()
