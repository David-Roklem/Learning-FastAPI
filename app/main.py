from fastapi import FastAPI

from models.basemodel import UserCreate, Feedback

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
