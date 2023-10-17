from fastapi import FastAPI

# from models.basemodel import User

app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    return fake_users.get(user_id, {"error": "User not found"})
