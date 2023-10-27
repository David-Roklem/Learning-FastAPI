# Быстрый старт в FastAPI Python
import random
import secrets
from typing import Annotated, Optional
from fastapi import (
    Cookie, FastAPI, HTTPException, Header, Response, Depends, status
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import jwt

from models.basemodel import User, Product, UserCreate, Feedback
from db.data import sample_products

app = FastAPI()
security = HTTPBasic()

fake_users = {
    1: {'username': 'john_doe', 'email': 'john@example.com'},
    2: {'username': 'jane_smith', 'email': 'jane@example.com'},
}

feedbacks = []


@app.get('/users/{user_id}')
def read_user(user_id: int):
    return fake_users.get(user_id, {'error': 'User not found'})


@app.post('/feedback')
def post_feedback(feedback: Feedback):
    name = feedback.name
    message = feedback.message
    feedbacks.append(dict(name=name, message=message))
    with open('file.txt', 'a', encoding='utf-8') as f:
        f.write(str(feedback) + '\n')
    answer = f'Feedback received. Thank you, {name}!'
    return {'message': answer}


@app.post('/create_user')
def create_user(user: UserCreate):
    user_id = len(fake_users) + 1
    fake_users.setdefault(
        user_id, dict(
            username=user.name,
            email=user.email,
            age=user.age,
            is_subscribed=user.is_subscribed
        )
    )
    print(fake_users)
    return fake_users.get(user_id, 'User not found')


# 3.1
@app.get('/product/{product_id}')
def get_product(product_id: int):
    for product in sample_products:
        if product['product_id'] == product_id:
            return product
    return {'error_message': 'product_not_found'}


@app.get('/products/search')
def find_products(keyword: str, category: str = None, limit: int = 10):
    if category:
        res = list(
            filter(
                lambda product: keyword.lower() in product['name'].lower()
                and category == product['category'], sample_products
            )
        )
    else:
        res = list(
            filter(
                lambda product: keyword.lower() in product['name'].lower(),
                sample_products
            )
        )
    return res[:limit]


# Для # 3.2. Задача на программирование
cookie_users = [
    {'username': 'user123', 'password': 'password123'}
]

sessions: dict = {}  # session db for storing cookie data


# # 3.2. Задача на программирование
# @app.post('/login')
# def login_user(user: User, response: Response):
#     for cookie_user in cookie_users:
#         if user.username == cookie_user.get('username')\
#                 and user.password == cookie_user.get('password'):
#             session_token = 'some unique token'
#             sessions[session_token] = user
#             response.set_cookie(
#                 key='session_token',
#                 value=session_token,
#                 httponly=True
#             )
#             return {'message': 'cookies has been cooked :)'}
#     return {'message': 'no such user'}


@app.get("/user")
def root(session_token: Optional[str] = Cookie(None)):
    user: User = sessions.get(session_token)
    if user:
        return user.model_dump()
    return {'message': 'Unauthorized'}


@app.get("/del_cookie")
def del_cookie(
    response: Response, session_token: Optional[str] = Cookie(None)
):
    user: User = sessions.get(session_token)
    if user:
        response.delete_cookie(key='session_token')
        return {'message': 'Deleted cookies'}
    return {'message': 'Unauthorized'}


# 3.3. Задача на программирование
@app.get('/headers')
def get_headers(
    user_agent: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None
):
    if not user_agent or not accept_language:
        raise HTTPException(detail='no headers', status_code=400)
    return {'User-Agent': user_agent, 'Accept-Language': accept_language}


# 4.1. Задача на программирование
def authenticate_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username = credentials.username
    correct_username = 'stanleyjobson'
    is_correct_username = secrets.compare_digest(
        current_username, correct_username
    )
    current_password = credentials.password
    correct_password = 'swordfish'
    is_correct_password = secrets.compare_digest(
        current_password, correct_password
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',

        )
    return credentials.username


@app.get('/login')
def read_current_user(username: Annotated[str, Depends(authenticate_user)]):
    return {'username': username}


# 4.2 Задача на программирование повышенной сложности
SECRET_KEY = '6074f205fde91252b3452b94045140356ae3a7e6e593c79062545554f6f6b26'
ALGORITHM = 'HS256'

USERS_DATA = [
    {'username': 'admin', 'password': 'adminpass'}
]


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@app.post('/login')
def is_authenticated(payload: dict):
    for user_data in USERS_DATA:
        if user_data.get('username') == payload['username']\
                and user_data.get('password') == payload['password']:
            return {
                'access_token': create_jwt_token(
                    {'sub': user_data['username']}
                )
            }
    return {'error': 'Invalid credentials'}


@app.get('/protected_resource')
def get_protected_res(authorization: Annotated[str | None, Header()] = None):
    if not authorization:
        raise HTTPException(
            detail='no Authorization header provided', status_code=400
        )
    try:
        decoded_token = jwt.decode(
            authorization, SECRET_KEY, algorithms=[ALGORITHM]
        )
    except jwt.InvalidTokenError:
        return {'error message': 'invalid credentials'}
    for user_data in USERS_DATA:
        if decoded_token['sub'] == user_data['username']:
            return {'message': 'access granted'}
    return {'error message': 'invalid credentials'}
