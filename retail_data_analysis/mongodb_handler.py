from pymongo import MongoClient
from bson.binary import Binary
import gridfs

class MongoDBHandler:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="retail_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)

    def insert_comment(self, product_id, comment):
        comments_collection = self.db['comments']
        comment_doc = {
            "product_id": product_id,
            "comment": comment
        }
        result = comments_collection.insert_one(comment_doc)
        return result.inserted_id

    def get_comments(self, product_id):
        comments_collection = self.db['comments']
        return list(comments_collection.find({"product_id": product_id}))

    def insert_image(self, product_id, image_data):
        # image_data should be bytes
        image_id = self.fs.put(image_data, filename=f"product_{product_id}_image")
        images_collection = self.db['images']
        images_collection.insert_one({
            "product_id": product_id,
            "image_id": image_id
        })
        return image_id

    def get_images(self, product_id):
        images_collection = self.db['images']
        image_docs = images_collection.find({"product_id": product_id})
        images = []
        for doc in image_docs:
            image_data = self.fs.get(doc['image_id']).read()
            images.append(image_data)
        return images

    def close(self):
        self.client.close()
