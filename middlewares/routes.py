# Import default modules
from urllib.parse import urlparse

# Actions list
actions = {
    '/registration': {
        'module': 'registration',
        'methods': ['POST'],
    },
    '/login': {
        'module': 'login',
        'methods': ['POST'],
    },

    '/items': {
        'module': 'items',
        'methods': ['GET'],
    },
    '/item':  {
        'module': 'item',
        'methods': ['GET', 'POST', 'PUT', 'DELETE'],
    },
}

# Run - Execute package for check module
def run(method, http):
    path = urlparse(http.path).path

    if path in actions:
        if actions[path]['methods'].count(method):
            return actions[path]['module']

        else:
            http.send_response(405)

            return

    else:
        http.send_response(404)

        return