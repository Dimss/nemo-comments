import falcon
import pymongo
import os
import json
from comments.middleware import AuthMiddleware, JSONTranslator

MONGO_HOST = os.environ['MONGO_HOST']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASS = os.environ['MONGO_PASS']
MONGO_DB = os.environ['MONGO_DB']
mongo_client = pymongo.MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/")
DB = mongo_client[MONGO_DB]


class CommentsResource:
    def on_get(self, req, resp, image_id):
        try:
            comments = list(DB.comments.find({'imageId': image_id}, {'_id': False, 'userId': False, 'imageId': False}))
            resp.body = json.dumps({'status': 'ok', 'data': comments})
        except Exception as ex:
            raise falcon.HTTPError(ex)

    def on_post(self, req, resp):
        try:
            record = req.context.get('doc')
            record['userId'] = req.context.get('user_identity')['sub']
            DB.comments.insert_one(record)
            resp.body = json.dumps({'status': 'ok', 'data': "New comment successfully created"})
        except Exception as ex:
            raise falcon.HTTPError(ex)


api = application = falcon.API(middleware=[JSONTranslator(), AuthMiddleware()])
api.add_route('/v1/comments', CommentsResource())
api.add_route('/v1/comments/{image_id}', CommentsResource())
