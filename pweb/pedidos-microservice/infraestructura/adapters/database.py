from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class PedidoModel(Base):
    __tablename__ = "pedidos"
    
    idpedido = Column(Integer, primary_key=True, index=True)
    idusuario = Column(Integer, nullable=False, index=True)
    fecha = Column(DateTime, default=datetime.now)
    estado = Column(String(20), default="pendiente")
    total = Column(Float, default=0.0)
    
    items = relationship("ItemPedidoModel", back_populates="pedido", cascade="all, delete-orphan")

class ItemPedidoModel(Base):
    __tablename__ = "items_pedido"
    
    iditem = Column(Integer, primary_key=True, index=True)
    idpedido = Column(Integer, ForeignKey("pedidos.idpedido"))
    producto = Column(String(100), nullable=False)
    cantidad = Column(Integer, default=1)
    precio = Column(Float, default=0.0)
    
    pedido = relationship("PedidoModel", back_populates="items")


DATABASE_URL = "sqlite:///./pedidos.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)