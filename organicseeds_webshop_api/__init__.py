# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
import string
from cornice.tests.support import CatchErrors
from colander import MappingSchema, SchemaNode, String
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from cornice import Service
from cornice.schemas import CorniceSchema

from organicseeds_webshop_api.resources import Root



def includeme(config):
    config.include("cornice")
    config.scan("organicseeds_webshop_api.categories")

# pyramid application main
def main(global_config, **settings):
    config = Configurator(settings={})
    config.set_root_factory(Root)

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
