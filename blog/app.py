import json

from pyramid import config, response

from blog import storage

def posts(request):
    engine = request.registry.settings['engine']
    posts = [(content, 'anonymous')
             for content, in storage.get_posts(engine)]
    body = json.dumps(posts).encode('utf-8')
    return response.Response(
               content_type='application/json',
               body=body)

def add_post(request):
    engine = request.registry.settings['engine']
    content = request.json_body['content']
    storage.add_post(engine, content)
    return response.Response('ok')

with config.Configurator() as cfg:
    engine = storage.get_engine()
    cfg.add_settings(dict(engine=engine))
    cfg.add_route('posts', '/posts',
                  request_method='GET')
    cfg.add_view(posts, route_name='posts')
    cfg.add_route('add_post', '/posts',
                  request_method='POST')
    cfg.add_view(add_post, route_name='add_post')
    app = cfg.make_wsgi_app()
