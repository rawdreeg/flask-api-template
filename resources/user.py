from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot be empty")

    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be empty")

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user:
            return {"message": "User exists"}, 400

        user = UserModel(**data)
        user.save_user_to_db()
        return {"message": "User created"}, 201

