# Import default modules
from urllib.parse import urlparse

# Actions list
actions = {
    '/items': {
        'GET': True,
    },
    '/item': {
        'GET': True, 'POST': True, 'PUT': True, 'DELETE': True,
    },
}

# Run - Execute module for check access in actions
def run(http, method, cursor):
    path = urlparse(http.path).path

    if path in actions and method in actions[path] and actions[path]:
        if not http.headers.get('Token'):
            http.send_response(401)

            return False

        cursor.execute('SELECT true FROM sessions WHERE token = %s AND enabled', [http.headers.get('Token')])

        if cursor.fetchone() is None:

            http.send_response(401)
            return False

    return True