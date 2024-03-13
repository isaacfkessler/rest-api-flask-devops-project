from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from flask_restful import reqparse
from mongoengine import NotUniqueError

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
        return jsonify(UserModel.objects())


class User(Resource):


    @staticmethod
    def validate_cpf(cpf):
        # Remove non-numeric characters
        cpf = ''.join(filter(str.isdigit, cpf))

        # Check if CPF has 11 digits
        if len(cpf) != 11:
            return False

        # Check if all digits are equal
        if cpf == cpf[0] * 11:
            return False

        # Calculate first verifier digit
        sum_ = sum(int(cpf[i]) * (10 - i) for i in range(9))
        remainder = sum_ % 11
        if remainder < 2:
            digit1 = 0
        else:
            digit1 = 11 - remainder

        # Verify first verifier digit
        if digit1 != int(cpf[9]):
            return False

        # Calculate second verifier digit
        sum_ = sum(int(cpf[i]) * (11 - i) for i in range(10))
        remainder = sum_ % 11
        if remainder < 2:
            digit2 = 0
        else:
            digit2 = 11 - remainder

        # Verify second verifier digit
        if digit2 != int(cpf[10]):
            return False

        return True

    def post(self):
        data = user_parse.parse_args()
        
        if not self.validate_cpf(data["cpf"]):
            return {"message": "CPF is invalid!"}, 400
        try:
            response = UserModel(**data).save()
            return {"message": "user %s sucessfully created!" % response.id}
        except NotUniqueError:
            return {"message": "CPF already exists in database!"}, 400

    def get(self, cpf):
        return jsonify(UserModel.objects(cpf=cpf))


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
