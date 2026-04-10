import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app


class User(UserMixin):
    def __init__(self, username: str) -> None:
        self.username = username
        self.id='1'  # For simplicity, we use a fixed ID for the admin user

    def __repr__(self) -> str:
        return f'<User {self.username}>'
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password,method='pbkdf2:sha256', salt_length=8)


    def set_hash(self, password_hash: str) -> None:
        self.password_hash = password_hash

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
class Graph(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64),unique=True)
    public: so.Mapped[bool] = so.mapped_column(sa.Boolean(),default=False)
    path: so.Mapped[str] = so.mapped_column(sa.String(128))

    def __repr__(self):
        return f"<Graph {self.name} with id {self.id}>"
    

    

@login.user_loader
def load_user(id: str) -> User:
    user= current_app.config['ADMIN_USER'] if id == "1" else None
    return user