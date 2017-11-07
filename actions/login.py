import re
import time
from hashlib import sha1

def POST(parameters, cursor):
    if 'email' not in parameters or re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", parameters['email']) is None:
        return (400, None)

    if 'password' not in parameters or len(parameters['password']) < 4:
        return (400, None)

    parameters['password'] = sha1(parameters['password'].encode('utf-8')).hexdigest()

    SQL = "SELECT id FROM users WHERE email = %(email)s AND password = %(password)s"

    cursor.execute(SQL, parameters)

    result = cursor.fetchone()

    if result is None:
        return (404, None)

    SQL = "UPDATE sessions SET enabled = false WHERE user_id = %s"

    cursor.execute(SQL, [result.id])

    token = sha1((str(result.id) + ' \ ' + str(time.time())).encode('utf-8')).hexdigest()

    SQL = "INSERT INTO sessions (user_id, token) VALUES (%s, %s)"

    cursor.execute(SQL, [result.id, token])

    return (200, {'token': token})