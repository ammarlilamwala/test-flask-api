# -*- coding: utf-8 -*-

# -- Public Imports
import sqlite3
from flask_restful import Resource, reqparse

# -- Private Imports
from models.user import UserModel

# -- Class
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username - mandatory')
    parser.add_argument('password', type=str, required=True, help='Password - mandatory')

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "username '{0}' already exists".format(data['username'])}
        
        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message':'user {0} created'.format(data['username'])}, 201
