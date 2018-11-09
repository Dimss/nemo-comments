import falcon
import json
import jwt


class JSONTranslator(object):
    def process_request(self, req, resp):
        body = req.stream.read()
        if body:
            req.context['doc'] = json.loads(body)


class AuthMiddleware(object):

    def process_request(self, req, resp):
        if 'X-NEMO-AUTH' not in req.headers:
            raise falcon.HTTPUnauthorized('Missing auth token')
        auth_token = req.headers.get('X-NEMO-AUTH')
        user_identity = jwt.decode(auth_token, 'secret')
        req.context['user_identity'] = user_identity
