import re
from hashlib import sha1

def POST(parameters, cursor):
    if 'name' not in parameters or len(parameters['name']) < 5:
        return (400, None)

    if 'email' not in parameters or re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", parameters['email']) is None:
        return (400, None)

    if 'password' not in parameters or len(parameters['password']) < 4:
        return (400, None)

    SQL = "SELECT true FROM users WHERE email = %s"

    cursor.execute(SQL, [parameters['email']])

    if cursor.fetchone() is not None:
        return (409, None)

    parameters['password'] = sha1(parameters['password'].encode('utf-8')).hexdigest()

    SQL = "INSERT INTO users (name, email, password) VALUES (%(name)s, %(email)s, %(password)s)"

    cursor.execute(SQL, parameters)

    return (201, None)