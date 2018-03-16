from pyramid import config, response

def hello_world(request):
    return response.Response('Hello World!')

with config.Configurator() as cfg:
    cfg.add_route('hello', '/')
    cfg.add_view(hello_world, route_name='hello')
    app = cfg.make_wsgi_app()
