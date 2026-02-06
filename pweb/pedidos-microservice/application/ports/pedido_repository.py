from abc import ABC, abstractmethod
from typing import List, Optional
from domain.core.pedido import Pedido

class PedidoRepository(ABC):
    
    @abstractmethod
    def guardar(self, pedido: Pedido) -> Pedido:
        pass
    
    @abstractmethod
    def obtener_por_id(self, idpedido: int) -> Optional[Pedido]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Pedido]:
        pass
    
    @abstractmethod
    def obtener_por_usuario(self, idusuario: int) -> List[Pedido]:
        pass
    
    @abstractmethod
    def actualizar(self, pedido: Pedido) -> Optional[Pedido]:
        pass
    
    @abstractmethod
    def eliminar(self, idpedido: int) -> bool:
        pass
    
    @abstractmethod
    def actualizar_estado(self, idpedido: int, estado: str) -> Optional[Pedido]:
        pass