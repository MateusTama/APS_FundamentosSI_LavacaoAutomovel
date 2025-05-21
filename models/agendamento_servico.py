from db import get_connection

class AgendamentoServico:
    def __init__(self, id=None, veiculo_tipo_id=None, veiculo_tipo_nome=None, cliente_id=None, cliente_nome=None, servico_id=None, servico_nome=None, servico_preco=None, servico_duracao_estimada=None, colaborador_id=None, colaborador_nome=None, data_hora_cadastro=None, data_hora_agendamento=None, data_hora_inicio=None, data_hora_termino=None, status_id=None, status_descricao=None):
        self.id = id
        self.veiculo_tipo_id = veiculo_tipo_id
        self.veiculo_tipo_nome = veiculo_tipo_nome
        self.cliente_id = cliente_id
        self.cliente_nome = cliente_nome
        self.servico_id = servico_id
        self.servico_nome = servico_nome
        self.servico_preco = servico_preco
        self.servico_duracao_estimada = servico_duracao_estimada
        self.colaborador_id = colaborador_id
        self.colaborador_nome = colaborador_nome
        self.data_hora_cadastro = data_hora_cadastro
        self.data_hora_agendamento = data_hora_agendamento
        self.data_hora_inicio = data_hora_inicio
        self.data_hora_termino = data_hora_termino
        self.status_id = status_id
        self.status_descricao = status_descricao

    def inserir(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO agendamento_servico
            (veiculo_tipo_id, cliente_id, servico_id, datahora_agendamento, status_id)
            VALUES
            (%s, %s, %s, %s, %s)            
        """, (self.veiculo_tipo_id, self.cliente_id, self.servico_id, self.data_hora_agendamento, self.status_id))

        conn.commit()
        cursor.close()
        conn.close()

    def buscar_todos_servicos_agendados(data_filtro=None, status_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        params = []

        query = """
            SELECT agendamento_id, agendamento_servico.veiculo_tipo_id, veiculo_tipo.veiculo_tipo_nome, agendamento_servico.cliente_id, cliente.usuario_nome, agendamento_servico.servico_id, servico.servico_nome, servico.servico_preco, servico.servico_duracao_estimada, colaborador_id, colaborador.usuario_nome, datahora_cadastro, datahora_agendamento, datahora_inicio, datahora_termino, status_id, agendamento_servico_status.agendamento_servico_status_descricao
            FROM agendamento_servico
            INNER JOIN veiculo_tipo
            ON veiculo_tipo.veiculo_tipo_id = agendamento_servico.veiculo_tipo_id
            INNER JOIN usuario AS cliente
            ON cliente.usuario_id = agendamento_servico.cliente_id
            INNER JOIN servico
            ON servico.servico_id = agendamento_servico.servico_id
            INNER JOIN agendamento_servico_status
            ON agendamento_servico_status.agendamento_servico_status_id = agendamento_servico.status_id
            LEFT JOIN usuario AS colaborador
			ON colaborador.usuario_id = agendamento_servico.colaborador_id
        """

        if data_filtro:
            query += " AND DATE(datahora_agendamento) = %s"
            params.append(data_filtro)

        if status_id:
            query += " AND status_id = %s"
            params.append(status_id)

        cursor.execute(query, params)

        resultados = cursor.fetchall()
        servicos_agendados = []
        for registro in resultados:
            servico_agendado = AgendamentoServico(id=registro[0], veiculo_tipo_id=registro[1], veiculo_tipo_nome=registro[2], cliente_id=registro[3], cliente_nome=registro[4], servico_id=registro[5], servico_nome=registro[6], servico_preco=registro[7], servico_duracao_estimada=registro[8],colaborador_id=registro[9], colaborador_nome=registro[10], data_hora_cadastro=registro[11], data_hora_agendamento=registro[12], data_hora_inicio=registro[13], data_hora_termino=registro[14], status_id=registro[15], status_descricao=registro[16])
            servicos_agendados.append(servico_agendado)

        cursor.close()
        conn.close()

        if servicos_agendados:
            return servicos_agendados

        return None
    
    def buscar(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT agendamento_id, agendamento_servico.veiculo_tipo_id, veiculo_tipo.veiculo_tipo_nome, agendamento_servico.cliente_id, usuario.usuario_nome, agendamento_servico.servico_id, servico.servico_nome, colaborador_id, datahora_cadastro, datahora_agendamento, datahora_inicio, datahora_termino, status_id, agendamento_servico_status.agendamento_servico_status_descricao
            FROM agendamento_servico
            INNER JOIN veiculo_tipo
            ON veiculo_tipo.veiculo_tipo_id = agendamento_servico.veiculo_tipo_id
            INNER JOIN usuario 
            ON usuario.usuario_id = agendamento_servico.cliente_id
            INNER JOIN servico
            ON servico.servico_id = agendamento_servico.servico_id
            INNER JOIN agendamento_servico_status
            ON agendamento_servico_status.agendamento_servico_status_id = agendamento_servico.status_id
            WHERE agendamento_id = %s
        """, (id,))

        registro = cursor.fetchone()

        cursor.close()
        conn.close()

        if registro:
            # id = registro[0] igual ao parâmetro id 
            veiculo_tipo_id = registro[1]
            veiculo_tipo_nome = registro[2]
            cliente_id = registro[3]
            cliente_nome = registro[4] 
            servico_id = registro[5]
            servico_nome = registro[6]
            colaborador_id = registro[7]
            data_hora_cadastro = registro[8]
            data_hora_agendamento = registro[9]
            data_hora_inicio = registro[10]
            data_hora_termino = registro[11]
            status_id = registro[12]
            status_descricao = registro[13]

            return AgendamentoServico(id=id, veiculo_tipo_id=veiculo_tipo_id, veiculo_tipo_nome=veiculo_tipo_nome, cliente_id=cliente_id, cliente_nome=cliente_nome, servico_id=servico_id, servico_nome=servico_nome, colaborador_id=colaborador_id, data_hora_cadastro=data_hora_cadastro, data_hora_agendamento=data_hora_agendamento, data_hora_inicio=data_hora_inicio, data_hora_termino=data_hora_termino, status_id=status_id, status_descricao=status_descricao)
        
        return None
    
    def buscar_servicos_agendados_usuario(id, data_filtro=None):
        conn = get_connection()
        cursor = conn.cursor()

        params = []

        query = """
            SELECT agendamento_id, agendamento_servico.veiculo_tipo_id, veiculo_tipo.veiculo_tipo_nome, agendamento_servico.cliente_id, usuario.usuario_nome, agendamento_servico.servico_id, servico.servico_nome, colaborador_id, datahora_cadastro, datahora_agendamento, datahora_inicio, datahora_termino, status_id, agendamento_servico_status.agendamento_servico_status_descricao
            FROM agendamento_servico
            INNER JOIN veiculo_tipo
            ON veiculo_tipo.veiculo_tipo_id = agendamento_servico.veiculo_tipo_id
            INNER JOIN usuario 
            ON usuario.usuario_id = agendamento_servico.cliente_id
            INNER JOIN servico
            ON servico.servico_id = agendamento_servico.servico_id
            INNER JOIN agendamento_servico_status
            ON agendamento_servico_status.agendamento_servico_status_id = agendamento_servico.status_id
            WHERE cliente_id = %s
            ORDER BY datahora_agendamento      
        """

        params.append(id)

        if data_filtro:
            query += "AND DATE(datahora_agendamento) = %s"
            params.append(data_filtro)

        cursor.execute(query, params)

        resultados = cursor.fetchall()
        
        cursor.close()
        conn.close()

        servicos_agendados_usuario = []
        for registro in resultados:
            agendamento_id = registro[0] 
            veiculo_tipo_id = registro[1]
            veiculo_tipo_nome = registro[2]
            # cliente_id = registro[3] id já é o do cliente
            cliente_nome = registro[4] 
            servico_id = registro[5]
            servico_nome = registro[6]
            colaborador_id = registro[7]
            data_hora_cadastro = registro[8]
            data_hora_agendamento = registro[9]
            data_hora_inicio = registro[10]
            data_hora_termino = registro[11]
            status_id = registro[12]
            status_descricao = registro[13]

            servico_agendado = AgendamentoServico(id=agendamento_id, veiculo_tipo_id=veiculo_tipo_id, veiculo_tipo_nome=veiculo_tipo_nome, cliente_id=id, cliente_nome=cliente_nome, servico_id=servico_id, servico_nome=servico_nome, colaborador_id=colaborador_id, data_hora_cadastro=data_hora_cadastro, data_hora_agendamento=data_hora_agendamento, data_hora_inicio=data_hora_inicio, data_hora_termino=data_hora_termino, status_id=status_id, status_descricao=status_descricao)
            servicos_agendados_usuario.append(servico_agendado)

        if servicos_agendados_usuario:
            return servicos_agendados_usuario

        return None

    def cancelar_agendamento(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE agendamento_servico
            SET status_id = 3
            WHERE agendamento_id = %s
        """, (id,))

        conn.commit()
        cursor.close()
        conn.close()

    def finalizar_agendamento(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE agendamento_servico
            SET status_id = 2
            WHERE agendamento_id = %s
        """, (id,))

        cursor.execute("""
            UPDATE agendamento_servico
            SET datahora_termino = NOW()
            WHERE agendamento_id = %s
        """, (id,))

        conn.commit()
        cursor.close()
        conn.close()

    def iniciar_agendamento(id, colaborador_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE agendamento_servico
            SET status_id = 4
            WHERE agendamento_id = %s
        """, (id,))

        cursor.execute("""
            UPDATE agendamento_servico
            SET colaborador_id = %s
            WHERE agendamento_id = %s
        """, (colaborador_id, id))

        cursor.execute("""
            UPDATE agendamento_servico
            SET datahora_inicio = NOW()
            WHERE agendamento_id = %s
        """, (id,))

        conn.commit()
        cursor.close()
        conn.close()
