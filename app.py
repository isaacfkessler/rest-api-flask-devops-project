from flask import Flask
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from flask_restful import reqparse


app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = [
    {
        "db": "users",
        "host": "mongodb",
        "port": 27017,
        "username": "admin",
        "password": "isaacdevops"
    }
]


user_parse = reqparse.RequestParser()
user_parse.add_argument('first_name',
                    type=str,
                    required=True,
                    help='This field cannot be blank'
                    )
user_parse.add_argument('last_name',
                    type=str,
                    required=True,
                    help='This field cannot be blank'
                    )
user_parse.add_argument('email',
                    type=str,
                    required=True,
                    help='This field cannot be blank'
                    )
user_parse.add_argument('cpf',
                    type=str,
                    required=True,
                    help='This field cannot be blank'
                    )
user_parse.add_argument('birth_date',
                    type=str,
                    required=True,
                    help='This field cannot be blank'
                    )


api = Api(app)
db = MongoEngine(app)


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    birth_date = db.DateTimeField(required=True)


class Users(Resource):
    def get(self):
        return {'message': 'user 1'}


class User(Resource):
    def post(self):
        data = user_parse.parse_args()
        UserModel(**data).save()

    def get(self, cpf):
        return {'message': 'CPF'}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
