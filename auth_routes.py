from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth import AuthJWT

from schemas import Signupmodel, Loginmodel
from databace import session, engine
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

auth_routher = APIRouter()
session = session(bind=engine)


@auth_routher.get('/')
async def hello_root():
    return {'message': 'Bu auth route sign up sahifasi'}


@auth_routher.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: Signupmodel):
    db_email = session.query(UserModel).filter(UserModel.email == user.email).first()
    print(db_email)
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bu email allaqachon ro`yxatdan o`tilgan')

    dp_username = session.query(UserModel).filter(UserModel.username == user.username).first()

    if dp_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='Bu username allaqachon ro`yxatdan o`tilgan')

    new_user = UserModel(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    session.add(new_user)
    session.commit()
    data = {
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active
    }
    response_model = {
        'status': 'success',
        'message': 'Muvoffaqiyatli ro`yxatdan o`tdingiz',
        'data': data
    }
    return response_model


@auth_routher.post('/login', status_code=status.HTTP_200_OK)
def login(user: Loginmodel, Authorize: AuthJWT = Depends()):
    db_user = session.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username yoki parol xato')
