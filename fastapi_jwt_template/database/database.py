import warnings
from sqlmodel import Session, create_engine
from fastapi_jwt_template.models import models
from fastapi_jwt_template.config import settings
from sqlalchemy.exc import SAWarning
from sqlmodel.sql.expression import Select, SelectOfScalar

warnings.filterwarnings("ignore", category=SAWarning)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True


engine = create_engine(settings.database.url)

"""
Criacao dos modelos no banco de dados
"""
models.SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
