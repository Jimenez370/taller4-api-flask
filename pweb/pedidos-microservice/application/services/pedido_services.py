from typing import List, Optional
from domain.core.pedido import Pedido, ItemPedido
from application.ports.pedido_repository import PedidoRepository

class PedidoService:
    def __init__(self, repository: PedidoRepository):
        self.repository = repository
    
    def crear_pedido(self, idusuario: int, items: List[dict]) -> Pedido:
        if not idusuario:
            raise ValueError("ID de usuario es requerido")
        
        if not items:
            raise ValueError("El pedido debe tener al menos un item")
        
        pedido = Pedido(idusuario=idusuario)
        
        for item_data in items:
            pedido.agregar_item(
                producto=item_data.get('producto'),
                cantidad=item_data.get('cantidad', 1),
                precio=item_data.get('precio', 0.0)
            )
        
        return self.repository.guardar(pedido)
    
    def obtener_pedido(self, idpedido: int) -> Optional[Pedido]:
        return self.repository.obtener_por_id(idpedido)
    
    def obtener_todos_pedidos(self) -> List[Pedido]:
        return self.repository.obtener_todos()
    
    def obtener_pedidos_por_usuario(self, idusuario: int) -> List[Pedido]:
        return self.repository.obtener_por_usuario(idusuario)
    
    def actualizar_pedido(self, idpedido: int, items: Optional[List[dict]] = None) -> Optional[Pedido]:
        pedido = self.repository.obtener_por_id(idpedido)
        if not pedido:
            return None
        
        if items:
            pedido.items = []
            for item_data in items:
                item = ItemPedido(
                    producto=item_data.get('producto'),
                    cantidad=item_data.get('cantidad', 1),
                    precio=item_data.get('precio', 0.0)
                )
                pedido.items.append(item)
            pedido.calcular_total()
        
        return self.repository.actualizar(pedido)
    
    def actualizar_estado_pedido(self, idpedido: int, estado: str) -> Optional[Pedido]:
        estados_validos = ['pendiente', 'preparando', 'enviado', 'entregado', 'cancelado']
        if estado not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {estados_validos}")
        
        return self.repository.actualizar_estado(idpedido, estado)
    
    def eliminar_pedido(self, idpedido: int) -> bool:
        return self.repository.eliminar(idpedido)