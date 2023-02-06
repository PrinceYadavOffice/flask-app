import uuid
from db import stores
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request

blp = Blueprint('stores', __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    def get(self,store_id):    
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message="Store not found")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message":"Store deleted."}
        except:
            abort(404,message ="Store not found")

@blp.route("/store")
class StoreList(MethodView):

    def get(self):    
        return {"stores": list(stores.values())}
    
    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(
                400,
                message ="Bad request. Ensure name is included in JSON Payload"
            )
        
        for store in stores.values():
            if store_data['name']==store['name']:
                abort(400, message="store already exits.")        

        store_id = uuid.uuid4().hex
        store = {**store_data, "id":store_id}
        stores[store_id]=store    
        return store, 201





