from typing import List, Optional
from domain.user import User, UserCreate, UserUpdate, UserStatus
from application.ports.user_repository import UserRepository

class UserService:
    """Servicio de aplicación - implementa cosas de uso"""
    def __init__(self, user_repository: UserRepository):
        self.repository = repository

    def register_user(self, user_data: UserCreate) -> User:
        """Registra un nuevo usuario"""
        if not user_data.username or not user_data.email:
            raise ValueError("Username and email are required")

    #verificacion de unicidad del email
        existing_users = self.repository.find_by_email(user_data.email)
        if existing_users:
            raise ValueError(f"Email {user_data.email} is already in use")

    # crear uasuario
        return self.repository.save(user_data)
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por su ID"""
        return self.repository.find_by_id(user_id)

    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios"""
        return self.repository.find_all()

    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """Actualiza un usuario existente"""
        user = self.repository.find_by_id(user_id)
        if not user:
            return None

        #validar que el nuevo email no esta en uso para otros usuarios
        if user_update.email and user_update.email != user.email:
            existing_users = self.repository.find_by_email(user_update.email)
            if existing_users:
                raise ValueError(f"Email {user_update.email} is already in use")
            
        return self.repository.update(user_id, user_update)
    
    def delete_user(self, user_id: str) -> bool: 
        """Elimina un usuario por su ID"""
        return self.repository.delete(user_id)

    def desactivate_user(self, user_id: str) -> Optional[User]:
        """Desactiva un usuario"""
        user = self.repository.find_by_id(user_id)
        if not user:
            return None
        user.deactivate()
        return self.repository.update(user_id, UserUpdate(status=UserStatus.INACTIVE))

    def activate_user(self, user_id: str) -> Optional[User]: