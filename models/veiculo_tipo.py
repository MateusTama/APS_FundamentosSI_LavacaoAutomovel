from db import get_connection

class VeiculoTipo:
    def __init__(self, id=None, nome=None):
        self.id = id
        self.nome = nome

    def buscar_todos_tipos():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT veiculo_tipo_id, veiculo_tipo_nome 
            FROM  veiculo_tipo      
        """)

        resultados = cursor.fetchall()
        veiculo_tipos = []
        for registro in resultados:
            veiculo_tipo = VeiculoTipo(id=registro[0], nome=registro[1])
            veiculo_tipos.append(veiculo_tipo)

        cursor.close()
        conn.close()

        if veiculo_tipos:
            return veiculo_tipos

        return None