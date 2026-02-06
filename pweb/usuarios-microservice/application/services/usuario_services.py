from typing import List, Optional
from domain.core.usuario import Usuario
from application.ports.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository
    
    def crear_usuario(self, nombre: str, email: str) -> Usuario:
        if not nombre or not email:
            raise ValueError("Nombre y email son requeridos")
        
        if not '@' in email:
            raise ValueError("Email inválido")
        
        # Verificar si el email ya existe
        usuario_existente = self.repository.obtener_por_email(email)
        if usuario_existente:
            raise ValueError("El email ya está registrado")
        
        usuario = Usuario(nombre=nombre, email=email)
        return self.repository.guardar(usuario)
    
    def obtener_usuario(self, idusuario: int) -> Optional[Usuario]:
        return self.repository.obtener_por_id(idusuario)
    
    def obtener_todos_usuarios(self) -> List[Usuario]:
        return self.repository.obtener_todos()
    
    def actualizar_usuario(self, idusuario: int, nombre: Optional[str] = None, 
                          email: Optional[str] = None) -> Optional[Usuario]:
        usuario = self.repository.obtener_por_id(idusuario)
        if not usuario:
            return None
        
        if nombre:
            usuario.nombre = nombre
        if email:
            if not '@' in email:
                raise ValueError("Email inválido")
            usuario.email = email
        
        return self.repository.actualizar(usuario)
    
    def eliminar_usuario(self, idusuario: int) -> bool:
        return self.repository.eliminar(idusuario)
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return self.repository.obtener_por_email(email)