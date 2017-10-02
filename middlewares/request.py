# Import default modules
from urllib.parse import urlparse, parse_qs

import os, time, json

# Run - Execute module for prepare request
def run(method, http):
    parameters = {}

    if method == 'GET' or method == 'DELETE':
        query = parse_qs(urlparse(http.path).query, True)

        for key, value in query.items():
            if len(value) > 1:
                parameters[key] = value
            else:
                parameters[key] = value[-1]

    if method == 'POST' or method == 'PUT':
        if http.headers.get('content-length') is None:
            return {}

        length = int(http.headers.get('content-length'))

        if length == 0:
            return {}

        body = http.rfile.read(length)

        parameters = json.loads(body)

    path = 'logs/' + time.strftime('%Y_%m_%d')

    if not os.path.exists(path):
        os.makedirs(path)

    # Logs

    file = open(path + '/requests.log', 'a')

    data = time.strftime('%H:%M:%S') + ' ' + method + ' ' + urlparse(http.path).path

    if parameters:
        data = data + ' ' + json.dumps(parameters)

    file.write(data + '\n')

    file.close()

    # Result

    return parameters