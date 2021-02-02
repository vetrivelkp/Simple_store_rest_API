from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from resources.user import Userregistry
from resources.item import Item, Itemlist

app = Flask(__name__)
app.secret_key = 'Manjula'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Itemlist, '/items')
api.add_resource(Userregistry, '/register')

app.run(port=5000, debug=True)