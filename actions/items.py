def GET(parameters, cursor):
    cursor.execute('SELECT id, name, number, month, year FROM items')

    data = []

    result = cursor.fetchone()

    while result:
        data.append({
            'name': result.name,
            'number': result.number,
            'month': result.month,
            'year': result.year,
        })

        result = cursor.fetchone()

    return (200, data)