from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserBase, UserResponse
from core.security import get_password_hash

def update_profile(db: Session, user_data: UserBase) -> UserResponse:
    db_user = db.query(User).filter(User.email == user_email).first()
    if db_user:
        for var, value in vars(user_data).items():
            setattr(db_user, var, value) if value else None
        db.commit()
        db.refresh(db_user)
        return db_user

# Fonction de contrôleur pour réinitialiser le mot de passe de l'utilisateur
def reset_password(db: Session, email: str) -> bool:
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        # Logique de réinitialisation du mot de passe
        new_password = "new_password"  # Générer un nouveau mot de passe aléatoire
        db_user.hashed_password = get_password_hash(new_password)
        db.commit()
        return True
    return False

# Fonction de contrôleur pour mettre à jour le mot de passe de l'utilisateur
def update_password(db: Session, email: int, new_password: str) -> bool:
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        # Logique de mise à jour du mot de passe
        db_user.hashed_password = get_password_hash(new_password)
        db.commit()
        return True
    return False