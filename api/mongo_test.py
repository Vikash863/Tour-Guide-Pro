from .db import db

def test_mongo():
    print(db.list_collection_names())
