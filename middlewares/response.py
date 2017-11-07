# Import default modules
from urllib.parse import urlparse

import os, time, json

# Run - Execute package for prepare response
def run(method, http, code, body):
    http.send_response(code)

    http.send_header('Content-type','application/json')
    http.send_header('Access-Control-Allow-Origin','*')
    http.send_header('Access-Control-Allow-Headers', 'Token, Content-Type')
    http.send_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')
    http.end_headers()

    path = 'logs/' + time.strftime('%Y_%m_%d')

    if body is not None:
        http.wfile.write(bytes(json.dumps(body), "utf8"))

    # Logs

    if not os.path.exists(path):
        os.makedirs(path)

    file = open(path + '/responses.log', 'a')

    data = time.strftime('%H:%M:%S') + ' ' + method + ' ' + urlparse(http.path).path

    if body is not None:
        data = data + ' ' + json.dumps(body)

    file.write(data + '\n')

    file.close()