from db import db 

class ItemsModel(db.Model):
    __tablename__="items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique =False, nullable =False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")