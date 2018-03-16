import os

from zope import interface

from twisted.python import (usage, reflect,
                            threadpool, filepath)
from twisted import plugin
from twisted.application import (service,
                                 strports,
                                 internet)
from twisted.web import (wsgi, server,
                         static, resource)
from twisted.internet import reactor

import blog.app

class DelegatingResource(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, name, request):
        print("Got getChild", name, request)
        request.prepath = []
        request.postpath.insert(0, name)
        return self.wsgi_resource

def getRoot(pool):
    application = blog.app.app
    wsgi_resource = wsgi.WSGIResource(reactor,
                                      pool,
                                      application)
    root = DelegatingResource(wsgi_resource)
    static_resource = static.File('index.html')
    root.putChild(b'', static_resource)
    static_resource = static.File('static')
    root.putChild(b'static', static_resource)
    return root

def getPool(reactor):
    pool = threadpool.ThreadPool()
    reactor.callWhenRunning(pool.start)
    reactor.addSystemEventTrigger('after',
                                  'shutdown',
                                  pool.stop)
    return pool

class Options(usage.Options):
    pass

def makeService(options):
    pool = getPool(reactor)
    root = getRoot(pool)
    site = server.Site(root)
    ret = strports.service('tcp:8080', site)
    return ret
