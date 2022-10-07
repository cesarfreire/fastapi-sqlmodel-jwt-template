from datetime import timedelta
import time
from fastapi_jwt_template.auth.auth_handler import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    check_user,
    get_password_hash,
)
from fastapi_jwt_template.auth.auth_handler import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi_jwt_template.database.database import get_session

from fastapi_jwt_template.models.models import (
    User,
    UserOutSchema,
    UserInSchema,
    Token,
)
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()


# Adiciona o campo x-process-time na requisicao
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


#
#
# Rotas da API
#
#
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup", response_model=UserOutSchema)
def create_new_user(userIn: UserInSchema):
    # Verifica se o usuario ja existe
    user = check_user(userIn)
    if user:
        raise HTTPException(
            status_code=409,
            detail="Username and/or e-mail already exists",
        )
    with get_session() as session:
        new_user = User(
            username=userIn.username,
            email=userIn.email,
            full_name=userIn.full_name,
            hashed_password=get_password_hash(userIn.password),
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


@app.get("/users/me/", response_model=UserOutSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
