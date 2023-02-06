import uuid
from db import items
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request

from schemas import ItemSchema, ItemsUpdateSchema

blp = Blueprint("items",__name__, description="operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except:
            abort(404, message="Store not found")
    
    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted"}
        except:
            abort(404, message="Item not found")

    @blp.arguments(ItemsUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):              
        try:
            item = items[item_id]            
            item.update(item_data)            
            return item
        except:
            abort(404, message="Item not found")


@blp.route("/items/")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):        
        for item in items.values():
            if item_data['name'] == item['name'] and item_data['store_id'] == item['store_id']:
                abort(
                    400,
                    message = "Item already exits"
                )
        item_id = uuid.uuid4().hex
        item = {**item_data, "id":item_id}
        items[item_id]=item
        return item
