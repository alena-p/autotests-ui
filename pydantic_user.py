from pydantic import BaseModel

class User(BaseModel):
    id: int
    user_name: str
    email: str
    is_active: bool = True

user_data = {
    "id": 1,
    "user_name": "Joe",
    "email": "super.joe@gmail.com"
}

user = User(**user_data)

print(user)

