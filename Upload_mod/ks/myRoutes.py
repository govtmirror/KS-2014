"""
Using redirect route instead of simple routes since it supports strict_slash
Simple route: http://webapp-improved.appspot.com/guide/routing.html#simple-routes
RedirectRoute: http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
"""
from webapp2_extras.routes import RedirectRoute
from bp_includes import handlers as handlers
from myHandlers import *

from uploadrest import *
from upqueue import *


secure_scheme = 'https'

_routes = [ 
    RedirectRoute('/', UploadHandler),
    RedirectRoute('/uploadaward', PostAwardHandler),
    RedirectRoute('/upqueue', UpQueueHandler)
 ]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)
