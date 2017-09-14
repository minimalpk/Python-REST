from pprint import pprint

def GET(parameters, cursor):
    if 'id' not in parameters or not parameters['id'].isnumeric():
        return (400, None)

    cursor.execute('SELECT id, name, number, month, year FROM items WHERE id = %s', [parameters['id']])

    result = cursor.fetchone()

    return (200, {
        'name': result.name,
        'number': result.number,
        'month': result.month,
        'year': result.year,
    })

def POST(parameters, cursor):
    if 'name' not in parameters or len(parameters['name']) == 0:
        return (400, None)

    if 'number' not in parameters or len(parameters['number']) != 16:
        return (400, None)

    if 'month' not in parameters or len(parameters['month']) != 2:
        return (400, None)

    if 'year' not in parameters or len(parameters['year']) != 2:
        return (400, None)

    cursor.execute('INSERT INTO items (name, number, month, year) VALUES (%(name)s, %(number)s, %(month)s, %(year)s)', parameters)

    return (201, None)

def PUT(parameters, cursor):
    if 'id' not in parameters or not str(parameters['id']).isnumeric():
        return (400, None)

    if 'name' not in parameters or len(parameters['name']) == 0:
        return (400, None)

    cursor.execute('UPDATE items SET name = %(name)s WHERE id = %(id)s RETURNING true', parameters)

    if cursor.fetchone() is None:
        return (404, None)

    return (204, None)

def DELETE(parameters, cursor):
    if 'id' not in parameters or not parameters['id'].isnumeric():
        return (400, None)

    cursor.execute('DELETE FROM items WHERE id = %s RETURNING true', [parameters['id']])

    if cursor.fetchone() is None:
        return (404, None)

    return (204, None)