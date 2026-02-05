from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(BaseModel):
    '''Entidad de dominio: User'''
    id: str
    username: str
    email: str
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime

    def activate(self):
        """Comportamiento de dominio"""
        self.status = UserStatus.ACTIVE

    def deactivate(self):
        """Comportamiento de dominio"""
        self.status = UserStatus.INACTIVE

    def is_active(self) -> bool:
        """Comportamiento de dominio"""
        return self.status == UserStatus.ACTIVE
    
class UserCreate(BaseModel):
    """DTO para crear usuario"""
    username: str
    email: str

class UserUpdate(BaseModel):
    """DTO para actualizar usuario"""
    username: Optional[str] = None
    email: Optional[str] = None
    status: Optional[UserStatus] = None