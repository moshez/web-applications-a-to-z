import json

from pyramid import config, response

POSTS = [
    "Just chillin'",
    "Writing code",
    "Being awesome",
]

def posts(request):
    body = json.dumps(POSTS).encode('utf-8')
    return response.Response(
               content_type='application/json',
               body=body)

def add_post(request):
    POSTS.append(request.json_body['content'])
    return response.Response('ok')

with config.Configurator() as cfg:
    cfg.add_route('posts', '/posts',
                  request_method='GET')
    cfg.add_view(posts, route_name='posts')
    cfg.add_route('add_post', '/posts',
                  request_method='POST')
    cfg.add_view(add_post, route_name='add_post')
    app = cfg.make_wsgi_app()
