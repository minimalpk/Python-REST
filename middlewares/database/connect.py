# Import default packages
import psycopg2
import psycopg2.extras

DATABASE_USER     = "postgres"
DATABASE_PASSWORD = "12345"
DATABASE_NAME     = "development"


# Run - Execute module for connect in database
def run():
    database = psycopg2.connect("host='localhost' user='" + DATABASE_USER + "' password='" + DATABASE_PASSWORD + "' dbname='" + DATABASE_NAME + "'")

    database.autocommit = True    

    return {
        'database': database,
        'cursor': database.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
    }
