from fastapi import FastAPI

from models.basemodel import User

app = FastAPI()


@app.post('/user')
def user(request: User):
    return {
        'name': request.name,
        'age': request.age,
        'is_adult': is_adult(request.age)
    }


def is_adult(age: int):
    return age >= 18
