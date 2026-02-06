from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class ItemPedido:
    iditem: Optional[int] = None
    idpedido: Optional[int] = None
    producto: str = ""
    cantidad: int = 1
    precio: float = 0.0
    
    def total(self) -> float:
        return self.cantidad * self.precio

@dataclass
class Pedido:
    idpedido: Optional[int] = None
    idusuario: int = 0
    fecha: datetime = None
    estado: str = "pendiente"  # pendiente, preparando, enviado, entregado, cancelado
    total: float = 0.0
    items: List[ItemPedido] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.fecha is None:
            self.fecha = datetime.now()
    
    def calcular_total(self) -> float:
        self.total = sum(item.total() for item in self.items)
        return self.total
    
    def agregar_item(self, producto: str, cantidad: int, precio: float):
        item = ItemPedido(
            producto=producto,
            cantidad=cantidad,
            precio=precio
        )
        self.items.append(item)
        self.calcular_total()
    
    def es_valido(self) -> bool:
        return bool(self.idusuario and self.items)
    
    def __str__(self) -> str:
        return f"Pedido(id={self.idpedido}, usuario={self.idusuario}, total={self.total}, estado={self.estado})"