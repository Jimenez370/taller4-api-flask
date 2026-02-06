from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from domain.core.pedido import Pedido
from application.services.pedido_services import PedidoService
from infraestructura.adapters.pedido_repository_impl import PedidoRepositoryImpl

app = FastAPI(title="Microservicio de Pedidos")

# Dependencias
def get_pedido_service() -> PedidoService:
    repository = PedidoRepositoryImpl()
    return PedidoService(repository)

# Modelos Pydantic
class ItemPedidoCreate(BaseModel):
    producto: str
    cantidad: int = 1
    precio: float = 0.0

class PedidoCreate(BaseModel):
    idusuario: int
    items: List[ItemPedidoCreate]

class ItemPedidoResponse(BaseModel):
    iditem: Optional[int]
    producto: str
    cantidad: int
    precio: float
    
    class Config:
        from_attributes = True

class PedidoResponse(BaseModel):
    idpedido: int
    idusuario: int
    fecha: datetime
    estado: str
    total: float
    items: List[ItemPedidoResponse]
    
    @classmethod
    def from_domain(cls, pedido: Pedido):
        return cls(
            idpedido=pedido.idpedido,
            idusuario=pedido.idusuario,
            fecha=pedido.fecha,
            estado=pedido.estado,
            total=pedido.total,
            items=[
                ItemPedidoResponse(
                    iditem=item.iditem,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio=item.precio
                )
                for item in pedido.items
            ]
        )

# Rutas
@app.post("/pedidos/", response_model=PedidoResponse)
def crear_pedido(pedido_data: PedidoCreate, service: PedidoService = Depends(get_pedido_service)):
    try:
        items_dict = [item.dict() for item in pedido_data.items]
        pedido = service.crear_pedido(
            idusuario=pedido_data.idusuario,
            items=items_dict
        )
        return PedidoResponse.from_domain(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse)
def obtener_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    pedido = service.obtener_pedido(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return PedidoResponse.from_domain(pedido)

@app.get("/pedidos/", response_model=List[PedidoResponse])
def obtener_todos_pedidos(service: PedidoService = Depends(get_pedido_service)):
    pedidos = service.obtener_todos_pedidos()
    return [PedidoResponse.from_domain(p) for p in pedidos]

@app.get("/pedidos/usuario/{usuario_id}", response_model=List[PedidoResponse])
def obtener_pedidos_por_usuario(usuario_id: int, service: PedidoService = Depends(get_pedido_service)):
    pedidos = service.obtener_pedidos_por_usuario(usuario_id)
    return [PedidoResponse.from_domain(p) for p in pedidos]

@app.put("/pedidos/{pedido_id}", response_model=PedidoResponse)
def actualizar_pedido(pedido_id: int, items: List[ItemPedidoCreate], 
                     service: PedidoService = Depends(get_pedido_service)):
    try:
        items_dict = [item.dict() for item in items]
        pedido = service.actualizar_pedido(pedido_id, items_dict)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return PedidoResponse.from_domain(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/pedidos/{pedido_id}/estado")
def actualizar_estado_pedido(pedido_id: int, estado: str, service: PedidoService = Depends(get_pedido_service)):
    try:
        pedido = service.actualizar_estado_pedido(pedido_id, estado)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return PedidoResponse.from_domain(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    eliminado = service.eliminar_pedido(pedido_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"message": "Pedido eliminado correctamente"}