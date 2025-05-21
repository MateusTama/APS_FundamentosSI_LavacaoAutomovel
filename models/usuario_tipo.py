from db import get_connection

class UsuarioTipo:
    def __init__(self, id=None, perfil=None):
        self.id = id
        self.perfil = perfil

    def buscar(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT usuario_tipo_id, usuario_tipo_perfil 
            FROM usuario_tipo
            WHERE usuario_tipo_id = %s     
        """, (id,)
        )

        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if resultado:
            return UsuarioTipo(id=resultado[0], perfil=resultado[1])
        
        return None

    def buscar_por_perfil(perfil):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT usuario_tipo_id, usuario_tipo_perfil 
            FROM usuario_tipo
            WHERE usuario_tipo_perfil = %s     
        """, (perfil,)
        )

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:
            return UsuarioTipo(id=resultado[0], perfil=resultado[1])
        
        return None
    
    def is_admin(tipo_id):
        usuario_tipo = UsuarioTipo.buscar_por_perfil("Administrador")
        if usuario_tipo:
            if tipo_id == usuario_tipo.id:
                return True

        return False
    
    def is_funcionario(tipo_id):
        usuario_tipo = UsuarioTipo.buscar_por_perfil("Funcionario")
        if usuario_tipo:
            if tipo_id == usuario_tipo.id:
                return True

        return False
    
