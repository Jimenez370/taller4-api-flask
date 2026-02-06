from typing import List, Optional
from sqlalchemy.orm import Session
from domain.core.usuario import Usuario
from application.ports.usuario_repository import UsuarioRepository
from .database import SessionLocal, UsuarioModel

class UsuarioRepositoryImpl(UsuarioRepository):
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def guardar(self, usuario: Usuario) -> Usuario:
        db_usuario = UsuarioModel(
            nombre=usuario.nombre,
            email=usuario.email
        )
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        usuario.idusuario = db_usuario.idusuario
        return usuario
    
    def obtener_por_id(self, idusuario: int) -> Optional[Usuario]:
        db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.idusuario == idusuario).first()
        if db_usuario:
            return Usuario(
                idusuario=db_usuario.idusuario,
                nombre=db_usuario.nombre,
                email=db_usuario.email
            )
        return None
    
    def obtener_todos(self) -> List[Usuario]:
        db_usuarios = self.db.query(UsuarioModel).all()
        return [
            Usuario(
                idusuario=u.idusuario,
                nombre=u.nombre,
                email=u.email
            )
            for u in db_usuarios
        ]
    
    def actualizar(self, usuario: Usuario) -> Optional[Usuario]:
        db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.idusuario == usuario.idusuario).first()
        if db_usuario:
            db_usuario.nombre = usuario.nombre
            db_usuario.email = usuario.email
            self.db.commit()
            self.db.refresh(db_usuario)
            return usuario
        return None
    
    def eliminar(self, idusuario: int) -> bool:
        db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.idusuario == idusuario).first()
        if db_usuario:
            self.db.delete(db_usuario)
            self.db.commit()
            return True
        return False
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        if db_usuario:
            return Usuario(
                idusuario=db_usuario.idusuario,
                nombre=db_usuario.nombre,
                email=db_usuario.email
            )
        return None