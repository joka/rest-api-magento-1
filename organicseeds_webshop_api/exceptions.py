from webob import Response, exc
import json

###################
# errors          #
###################


class _500(exc.HTTPError):

    def __init__(self, msg='Internal Server Error'):
        body = {'status': "errors", 'errors': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 500
        self.content_type = 'application/json'


class WebshopAPIErrors(Exception):

    def __init__(self, errors, success):
        self.errors = errors
        self.success = success

    def __str__(self):
        return repr("WebshopAPIErrors: " + str(self.errors))
