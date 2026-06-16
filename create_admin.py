"""Script de création du compte administrateur."""
from infrastructure.database.session import SessionLocal, init_db
from infrastructure.database.models import UserModel
from infrastructure.auth.password_service import PasswordService

init_db()
db = SessionLocal()

username = "vainqueur"
password = "00Kalema"

# Vérifier si l'utilisateur existe déjà
existant = db.query(UserModel).filter(UserModel.username == username).first()
if existant:
    print("ℹ️  L'utilisateur admin existe déjà.")
else:
    user = UserModel(
        username=username,
        password_hash=PasswordService.hacher(password)
    )
    db.add(user)
    db.commit()
    print(f"✅ Utilisateur '{username}' créé avec le mot de passe '{password}'.")

db.close()