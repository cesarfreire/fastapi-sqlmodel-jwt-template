from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid as uuid_pkg

"""
Neste arquivo sao criados todos os modelos que sao utilizados na API
"""


# Classe para adicionar o UUID no usuario.
class UUIDModelBase(SQLModel):
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


# Classe principal dos usuarios
class User(UUIDModelBase, table=True):
    username: str
    email: EmailStr
    full_name: Optional[str] = ""
    hashed_password: Optional[str] = ""
    disabled: Optional[bool] = False


"""
Classe que eh utilizada para enviar os dados do usuario
para o GET, sem dados sensíveis
"""


class UserOutSchema(UUIDModelBase):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool


class UserInSchema(SQLModel):
    username: str
    email: EmailStr
    full_name: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
