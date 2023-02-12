from app import get_app
from flask import request, jsonify
from flask.views import MethodView
from models import Session, User, Post
from errors import HttpError
from schema import validate_create_user, validate_create_post
from sqlalchemy.exc import IntegrityError

app = get_app()


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def get_post(post_id: int, session: Session):
    post = session.query(Post).get(post_id)
    if post is None:
        raise HttpError(409, 'post not found')
    return post


class UserView(MethodView):

    def post(self):
        json_data = validate_create_user(request.json)
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'user already exists')
            return jsonify(
                {
                    'id': new_user.id,
                    'username': new_user.username
                }
            )

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            print(user)

            return jsonify({
                'id': user.id,
                'username': user.username
            })


class PostView(MethodView):
    def post(self):
        json_data = validate_create_post(request.json)
        with Session() as session:
            new_post = Post(**json_data)
            session.add(new_post)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'post already exists')
            return jsonify(
                {
                    'id': new_post.id,
                    'header': new_post.header,
                    'owner': new_post.owner
                }
            )

    def get(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)

            return jsonify({
                'id': post.id,
                'header': post.header,
                'description': post.description,

            })

    def delete(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)
            session.delete(post)
            session.commit()
            return {'deleted': 'true'}


app.add_url_rule('/users', view_func=UserView.as_view('users_with_id'), methods=['POST'])
app.add_url_rule('/post', view_func=PostView.as_view('create_post_with_id'), methods=['POST'])
app.add_url_rule('/post/<int:post_id>', view_func=PostView.as_view('post_with_id'), methods=['GET', 'DELETE'])
app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('user_with_id'), methods=['GET'])


app.run(port=5000)
