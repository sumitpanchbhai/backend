import psycopg2
import pandas as pd

class DBConnection():
    def __init__(self):
        self.connection = conn = psycopg2.connect(
            database="test_databse", user='postgres', password='sumit', host='127.0.0.1', port='5432')
    def get_connection(self):
        # establishing the connection
        if self.connection is not None:
            return self.connection
        else:
            return "Can't connect to database"
    def release_connection(self,connection):
        if connection is not None:
            return connection.close()

