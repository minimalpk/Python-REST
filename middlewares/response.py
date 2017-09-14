# Import default modules
import json

# Run - Execute package for prepare response
def run(http, code, body):
    http.send_response(code)

    http.send_header('Content-type','application/json')
    http.end_headers()

    if body is None:
        return

    http.wfile.write(bytes(json.dumps(body), "utf8"))