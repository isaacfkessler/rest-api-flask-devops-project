from flask import jsonify
from flask_restful import Resource, Api, reqparse
from mongoengine import NotUniqueError
from .model import UserModel, HealthCheckModel


user_parse = reqparse.RequestParser()
user_parse.add_argument(
    "first_name", type=str, required=True, help="This field cannot be blank"
)
user_parse.add_argument(
    "last_name", type=str, required=True, help="This field cannot be blank"
)
user_parse.add_argument(
    "email", type=str, required=True, help="This field cannot be blank"
)
user_parse.add_argument(
    "cpf", type=str, required=True, help="This field cannot be blank"
)
user_parse.add_argument(
    "birth_date", type=str, required=True, help="This field cannot be blank"
)


class HealthCheck(Resource):
    def get(self):
        response = HealthCheckModel.objects(status="health")
        if response:
            return "Healthy", 200
        else:
            HealthCheckModel(status="health").save()
            return "Healthy", 200


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    @staticmethod
    def validate_cpf(cpf):
        # Remove non-numeric characters
        cpf = "".join(filter(str.isdigit, cpf))

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
        response = UserModel.objects(cpf=cpf)

        if response:
            return jsonify(response)

        return {"message": "User does not exist in database!"}, 400

    def patch(self):
        data = user_parse.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"message": "CPF is invalid!"}, 400

        response = UserModel.objects(cpf=data.cpf)
        if response:
            response.update(**data)
            return {"message": "User updated!"}, 200
        else:
            return {"message": "User does not exist in database!"}, 400

    def delete(self, cpf):
        response = UserModel.objects(cpf=cpf)

        if response:
            response.delete()
            return {"message": "User deleted!"}, 200
        else:
            return {"message": "User does not exist in database!"}, 400
