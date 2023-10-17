from fastapi import FastAPI

from models.basemodel import User

app = FastAPI()

user1 = User(
    name='John Doe',
    id=1
)


@app.get('/users')
def read_root():
    return user1
