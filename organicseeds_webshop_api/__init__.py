# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
#from cornice.tests.support import CatchErrors

from organicseeds_webshop_api.resources import bootstrap
import organicseeds_webshop_api.resources


ZODB_APP_ROOT_ID = "webshop_api"


def root_factory(request):
    conn = get_connection(request)
    return bootstrap(conn.root(), ZODB_APP_ROOT_ID, request)


def includeme(config):
    config.include("cornice")
    config.scan("organicseeds_webshop_api.services")
    config.include(organicseeds_webshop_api.utilities)
    config.include(organicseeds_webshop_api.resources)


# pyramid application main
def main(global_config, **settings):
    settings = {"zodbconn.uri": "memory://"}
    config = Configurator(settings=settings)
    config.set_root_factory(root_factory)
    config.include("pyramid_zodbconn")
    config.include("pyramid_tm")
    config.include(includeme)

    #return CatchErrors(config.make_wsgi_app())
    return config.make_wsgi_app()


# non pyramid main
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    httpd = make_server('', 8000, app)
    print "Listening on port 8000...."
    httpd.serve_forever()
