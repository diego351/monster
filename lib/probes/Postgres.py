import psycopg2

class Postgres(object):
    def __init__(self,username,password,db):
        self.dbName = db
        self.connString = "host='localhost' dbname='%s' user='%s' password='%s'" %(self.dbName,username,password)
        self.conn = psycopg2.connect(self.connString)
        self.cursor = self.conn.cursor()
    def report(self):
        select = "SELECT * FROM pg_stat_database WHERE datname = '%s'" % self.dbName
        self.cursor.execute(select)
        return self.cursor.fetchone()   
