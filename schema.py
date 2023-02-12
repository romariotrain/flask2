from pydantic import BaseModel
from pydantic import ValidationError
from errors import HttpError


class CreateUser(BaseModel):

    username: str
    password: str


class CreatePost(BaseModel):

    header: str
    description: str
    owner: str


def validate_create_user(json_data):
    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())


def validate_create_post(json_data):
    try:
        post_schema = CreatePost(**json_data)
        return post_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())
