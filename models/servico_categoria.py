from db import get_connection

class ServicoCategoria:
    def __init__(self, id=None, nome=None):
        self.id = id
        self.nome = nome

    def buscar_todas_categorias():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT servico_categoria_id, servico_categoria_nome 
            FROM servico_categoria       
        """)

        resultados = cursor.fetchall()
        servico_categorias = []
        for registro in resultados:
            servico_categoria = ServicoCategoria(id=registro[0], nome=registro[1])
            servico_categorias.append(servico_categoria)

        cursor.close()
        conn.close()

        if servico_categorias:
            return servico_categorias

        return None