import psycopg2

class Postgres(object):
    def __init__(self,username,password,db):
        self.dbName = db
        self.connString = "host='localhost' dbname='%s' user='%s' password='%s'" %(self.dbName,username,password)
        self.conn = psycopg2.connect(self.connString)
        self.cursor = self.conn.cursor()
    def getCurrentData(self):
        select = "SELECT * FROM pg_stat_database WHERE datname = '%s'" % self.dbName
        self.cursor.execute(select)
        temp =  dict(self.cursor.fetchone())
        
        return {
                "returned": temp["tup_returned"],
                "fetched": temp["tup_fetched"],
                "inserted": temp["tup_inserted"],
                "updated": temp["tup_updated"],
                "deleted": temp["tup_deleted"],
                }

    def report(self):
        pass
        
