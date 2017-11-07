# Import default modules
from http.server import BaseHTTPRequestHandler, HTTPServer

# Import middlewares modules
from middlewares.database import connect    as middlewareDatabaseConnect
from middlewares.database import disconnect as middlewareDatabaseDisconnect
from middlewares          import request    as middlewareRequest
from middlewares          import routes     as middlewareRoutes
from middlewares          import access     as middlewareAccess
from middlewares          import response   as middlewareResponse

HTTP_HOST = 'localhost'
HTTP_PORT = 8080

# Response
def response(http, database, cursor):
    http.send_header('Access-Control-Allow-Origin','*')
    http.send_header('Access-Control-Allow-Headers', 'Token, Content-Type')
    http.send_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')
    http.end_headers()

    if database is not None and cursor is not None:
        middlewareDatabaseDisconnect.run(database, cursor)

# Execute action
def execute(method, name, parametes, cursor):
    action = getattr(__import__('actions', None, None, [name]), name)

    result = getattr(action, method)(parametes, cursor)

    return {
        'code': result[0],
        'body': result[1],
    }

# Hanle action func
def handler(method, http):
    # Middleware request
    parameters = middlewareRequest.run(method, http)

    # Middleware routes
    action = middlewareRoutes.run(method, http)

    if action is None:
        response(http, None, None)

        return

    # Middleware database connect
    result = middlewareDatabaseConnect.run()

    database = result['database']
    cursor = result['cursor']

    # Middleware access
    result = middlewareAccess.run(http, method, cursor)

    if not result:
        response(http, database, cursor)

        return

    # Execute

    result = execute(method, action, parameters, cursor)

    # Middleware response
    middlewareResponse.run(method, http, result['code'], result['body'])

    # Middleware database disconnect
    middlewareDatabaseDisconnect.run(database, cursor)

# Hanle action class
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        handler('GET', self)

    def do_POST(self):
        handler('POST', self)

    def do_PUT(self):
        handler('PUT', self)

    def do_DELETE(self):
        handler('DELETE', self)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Headers', 'Token, Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')
        self.end_headers()

# Run server
HTTPServer((HTTP_HOST, HTTP_PORT), Handler).serve_forever()