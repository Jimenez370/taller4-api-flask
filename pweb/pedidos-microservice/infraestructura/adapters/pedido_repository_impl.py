from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from domain.core.pedido import Pedido, ItemPedido
from application.ports.pedido_repository import PedidoRepository
from .database import SessionLocal, PedidoModel, ItemPedidoModel

class PedidoRepositoryImpl(PedidoRepository):
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def guardar(self, pedido: Pedido) -> Pedido:
        db_pedido = PedidoModel(
            idusuario=pedido.idusuario,
            fecha=pedido.fecha or datetime.now(),
            estado=pedido.estado,
            total=pedido.total
        )
        
        self.db.add(db_pedido)
        self.db.commit()
        self.db.refresh(db_pedido)
        
        # Guardar items
        for item in pedido.items:
            db_item = ItemPedidoModel(
                idpedido=db_pedido.idpedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.precio
            )
            self.db.add(db_item)
        
        self.db.commit()
        
        pedido.idpedido = db_pedido.idpedido
        return pedido
    
    def obtener_por_id(self, idpedido: int) -> Optional[Pedido]:
        db_pedido = self.db.query(PedidoModel).filter(PedidoModel.idpedido == idpedido).first()
        if not db_pedido:
            return None
        
        return self._convertir_a_domain(db_pedido)
    
    def obtener_todos(self) -> List[Pedido]:
        db_pedidos = self.db.query(PedidoModel).all()
        return [self._convertir_a_domain(p) for p in db_pedidos]
    
    def obtener_por_usuario(self, idusuario: int) -> List[Pedido]:
        db_pedidos = self.db.query(PedidoModel).filter(PedidoModel.idusuario == idusuario).all()
        return [self._convertir_a_domain(p) for p in db_pedidos]
    
    def actualizar(self, pedido: Pedido) -> Optional[Pedido]:
        db_pedido = self.db.query(PedidoModel).filter(PedidoModel.idpedido == pedido.idpedido).first()
        if not db_pedido:
            return None
        
        # Actualizar datos básicos
        db_pedido.estado = pedido.estado
        db_pedido.total = pedido.total
        
        # Eliminar items antiguos y agregar nuevos
        self.db.query(ItemPedidoModel).filter(ItemPedidoModel.idpedido == pedido.idpedido).delete()
        
        for item in pedido.items:
            db_item = ItemPedidoModel(
                idpedido=pedido.idpedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.precio
            )
            self.db.add(db_item)
        
        self.db.commit()
        self.db.refresh(db_pedido)
        
        return pedido
    
    def actualizar_estado(self, idpedido: int, estado: str) -> Optional[Pedido]:
        db_pedido = self.db.query(PedidoModel).filter(PedidoModel.idpedido == idpedido).first()
        if not db_pedido:
            return None
        
        db_pedido.estado = estado
        self.db.commit()
        self.db.refresh(db_pedido)
        
        return self._convertir_a_domain(db_pedido)
    
    def eliminar(self, idpedido: int) -> bool:
        db_pedido = self.db.query(PedidoModel).filter(PedidoModel.idpedido == idpedido).first()
        if db_pedido:
            self.db.delete(db_pedido)
            self.db.commit()
            return True
        return False
    
    def _convertir_a_domain(self, db_pedido: PedidoModel) -> Pedido:
        items = []
        for db_item in db_pedido.items:
            items.append(ItemPedido(
                iditem=db_item.iditem,
                idpedido=db_item.idpedido,
                producto=db_item.producto,
                cantidad=db_item.cantidad,
                precio=db_item.precio
            ))
        
        return Pedido(
            idpedido=db_pedido.idpedido,
            idusuario=db_pedido.idusuario,
            fecha=db_pedido.fecha,
            estado=db_pedido.estado,
            total=db_pedido.total,
            items=items
        )