import psycopg2
from configparser import ConfigParser


class DBConnections():
    def get_postgres_creds(self, header):
        config = ConfigParser()

        # parse existing file
        try:
            config.read('properties.ini')
        except Exception as error:
            print(error)

        # read values from a section
        try:
            DB_NAME = config.get(header, 'DB_NAME')
            DB_USERNAME = config.get(header, 'DB_USERNAME')
            DB_PASSWORD = config.get(header, 'DB_PASSWORD')
            DB_HOST = config.get(header, 'DB_HOST')
            DB_PORT = config.get(header, 'DB_PORT')

            return {'DB_NAME': DB_NAME, 'DB_USERNAME': DB_USERNAME, 'DB_PASSWORD': DB_PASSWORD, 'DB_HOST': DB_HOST,
                    'DB_PORT': DB_PORT}
        except Exception as error:
            print(error)

    def get_db_connection(self):
        db_data = self.get_postgres_creds('postgres_connection')
        conn = psycopg2.connect(host=db_data['DB_HOST'],
                                database=db_data['DB_NAME'],
                                user=db_data['DB_USERNAME'],
                                password=db_data['DB_PASSWORD'])
        return conn
