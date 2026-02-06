from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    idusuario: Optional[int] = None
    nombre: str = ""
    email: str = ""
    
    def es_valido(self) -> bool:
        return bool(self.nombre and self.email and '@' in self.email)
    
    def __str__(self) -> str:
        return f"Usuario(id={self.idusuario}, nombre={self.nombre}, email={self.email})"