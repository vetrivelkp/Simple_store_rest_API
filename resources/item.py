import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, JWT
from models.items import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required = True, help = "This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message":"Item {} already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occured while trying to insert the item into database"}

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect("mydata.db")
        cursor = connection.cursor()

        delete_sql = "DELETE FROM items WHERE name = ?"

        cursor.execute(delete_sql, (name,))
        connection.commit()
        connection.close()
        return {'message': 'item deleted'}

    def put(self, name):
        #data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        upd_item = ItemModel(name, data['price'])

        if item:
            try:
                upd_item.update()
            except:
                return {"message": "An error occured while trying to update the item in database"}, 500
            return upd_item.json()
        else:
            try:
                upd_item.insert()
            except:
                return {"message": "An error occured while trying to insert the item into database"}, 500
            return upd_item.json(), 201

class Itemlist(Resource):
    def get(self):
        connection = sqlite3.connect("mydata.db")
        cursor = connection.cursor()

        select_all_sql = "SELECT * FROM items"
        result = cursor.execute(select_all_sql)
        items=[]
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        connection.close()
        return {'items':items}