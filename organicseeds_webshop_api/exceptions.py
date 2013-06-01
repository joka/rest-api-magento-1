from webob import Response, exc
import json

###################
# errors          #
###################


class _500(exc.HTTPError):

    code = 500
    title = "Internal Server Error"


class HTTPErrorJSON(exc.HTTPError):

    code = 200
    title = "OK"
    content_type = 'application/json'

    def __init__(self, msgs=[('location',
                              'name',
                              'description')]):
        super(HTTPErrorJSON, self).__init__()
        msgs_ = []
        for loc, name, desc in msgs:
            msgs_.append({"location": loc, "name": name, "description": desc})
        body = {'status': "errors", 'errors': msgs_}
        Response.__init__(self, body=json.dumps(body), status=self.code)


class _400(HTTPErrorJSON):
    """Bad Request Data"""

    code = 400
    title = "Bad Request Data"


class _502(HTTPErrorJSON):
    """Bad Gateway, error while communicating with Webshop"""

    code = 502
    title = "Bad Gateway, error while communicating with Webshop"
    success = []
    errors = []

    def __init__(self, msgs, errors=[], success=[]):
        super(_502, self).__init__(msgs)
        self.success = success
        self.errors = errors
