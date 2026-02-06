from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from domain.core.usuario import Usuario
from application.services.usuario_services import UsuarioService
from infraestructura.adapters.usuario_repository_impl import UsuarioRepositoryImpl

app = FastAPI(title="Microservicio de Usuarios")

# Dependencias
def get_usuario_service() -> UsuarioService:
    repository = UsuarioRepositoryImpl()
    return UsuarioService(repository)

# Modelos Pydantic
class UsuarioCreate(BaseModel):
    nombre: str
    email: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None

class UsuarioResponse(BaseModel):
    idusuario: int
    nombre: str
    email: str
    
    @classmethod
    def from_domain(cls, usuario: Usuario):
        return cls(
            idusuario=usuario.idusuario,
            nombre=usuario.nombre,
            email=usuario.email
        )

# Rutas
@app.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario(usuario_data: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    try:
        usuario = service.crear_usuario(
            nombre=usuario_data.nombre,
            email=usuario_data.email
        )
        return UsuarioResponse.from_domain(usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.from_domain(usuario)

@app.get("/usuarios/", response_model=List[UsuarioResponse])
def obtener_todos_usuarios(service: UsuarioService = Depends(get_usuario_service)):
    usuarios = service.obtener_todos_usuarios()
    return [UsuarioResponse.from_domain(u) for u in usuarios]

@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, 
                      service: UsuarioService = Depends(get_usuario_service)):
    try:
        usuario = service.actualizar_usuario(
            idusuario=usuario_id,
            nombre=usuario_data.nombre,
            email=usuario_data.email
        )
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return UsuarioResponse.from_domain(usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):
    eliminado = service.eliminar_usuario(usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}

@app.get("/usuarios/email/{email}", response_model=UsuarioResponse)
def buscar_usuario_por_email(email: str, service: UsuarioService = Depends(get_usuario_service)):
    usuario = service.buscar_por_email(email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.from_domain(usuario)