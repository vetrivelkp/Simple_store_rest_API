import sqlite3
from flask_restful import Resource, request, reqparse
from models.user import UserModel

class Userregistry(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type = str, required=True, help = "This field cannot be left black")
    parser.add_argument('password', type = str, required=True, help = "This field cannot be left black")
    def post(self):
        #data = request.get_json()
        data = Userregistry.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists'}, 400

        connection = sqlite3.connect("mydata.db")
        cursor = connection.cursor()

        ins_sql = "INSERT INTO users VALUES (NULL, ?, ?)"

        #user = User.find_by_username(data['username'])
        
        cursor.execute(ins_sql, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {'message': 'User created successfully'}