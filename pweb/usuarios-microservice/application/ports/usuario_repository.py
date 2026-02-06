from abc import ABC, abstractmethod
from typing import List, Optional
from domain.core.usuario import Usuario

class UsuarioRepository(ABC):
    
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        pass
    
    @abstractmethod
    def obtener_por_id(self, idusuario: int) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        pass
    
    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def eliminar(self, idusuario: int) -> bool:
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass