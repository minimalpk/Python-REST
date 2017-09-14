# Run - Execute module for disconnect in database
def run(database, cursor):
    cursor.close()
    database.close()