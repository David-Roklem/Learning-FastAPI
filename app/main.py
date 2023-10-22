from fastapi import FastAPI

from models.basemodel import Product, UserCreate, Feedback
from db.data import sample_products

app = FastAPI()

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
