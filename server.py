from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('UserID', required=True)
        parser.add_argument('Name', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['UserID'] in list(data['UserID']):
            return {
                'message': f"'{args['UserID']}' already Exists"
            }, 401
        else:
            new_data = pd.DataFrame({
                'UserID': args['UserID'],
                'Name': args['Name']
            })

            data = data.append(new_data, ignore_index=True)

            data.to_csv('users.csv', index=False)

            return {'data': data.to_dict()}, 200

class User(Resource):
    def get(self, UserID):
        ids = []
        index = ''
        datas = pd.read_csv('users.csv').to_dict()
        for uid in datas['UserID']:
            ids.append(uid)
        for i in ids:
            if UserID == datas['UserID'][i]:
                index = i
        return {"data": {"UserID": {"0": UserID}, "Name": {"0": datas['Name'][index]}}}, 200

app = Flask("Struct_API")
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(User, "/users/<string:UserID>")

if __name__ == '__main__':
    app.run("0.0.0.0",80, False)