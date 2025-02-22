import psycopg2 as pg
from configparser import ConfigParser

class DatabaseConnection:
    def __init__(self, filename='database.ini', section='postgresql'):
        self.filename = filename
        self.section = section

    def config(self):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))

        return db

    def connect(self):
        # Initialize connection
        conn = None

        try:
            # read connection parameters
            params = self.config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = pg.connect(**params)
            return conn

        except (Exception, pg.DatabaseError) as error:
            print(error)
            return None
