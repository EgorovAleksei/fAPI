from users.schemas import CreateUser

def create_user(user_in: CreateUser):
    user = user_in.model_dump()
    print(user)
    return {
        "success": True,
        "user": user,
    }