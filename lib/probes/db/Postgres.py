class Postgres(object):
    def __init__(self, options):

        try:
            import psycopg2
            import psycopg2.extras
            self.pg = psycopg2
            self.pg.extras = psycopg2.extras
        except ImportError:
            raise Exception("Psycopg missing, but postgres probe selected..")

        self.database = options.get('db')
        self.username = options.get('username')
        self.password = options.get('password')

        self.connString = "host='localhost' dbname='%s' user='%s' password='%s'" % (self.database,
                                                                                    self.username,
                                                                                    self.password)

        self.conn = self.pg.connect(self.connString)
        self.conn.autocommit = True
        self.firstTime = True
        self.emptyDict = {
                            "returned": 0,
                            "fetched": 0,
                            "inserted": 0,
                            "updated": 0,
                            "deleted": 0,
                            }

    def getCurrentData(self):
        cursor = self.conn.cursor(cursor_factory=self.pg.extras.RealDictCursor)
        select = "SELECT * FROM pg_stat_database WHERE datname = '%s'" % self.database
        cursor.execute(select)
        temp = cursor.fetchone()
        return {
                "returned": int(str(temp["tup_returned"])),
                "fetched":  int(str(temp["tup_fetched"])),
                "inserted": int(str(temp["tup_inserted"])),
                "updated":  int(str(temp["tup_updated"])),
                "deleted": int(str(temp["tup_deleted"])),
                }
    def report(self):
        if self.firstTime:
            self.myBuffer = self.getCurrentData()
            self.firstTime = False
            return self.emptyDict
        else:
            curr = self.getCurrentData()
            toRet = self.subtractDictValues(curr,self.myBuffer)
            self.myBuffer = curr
            return toRet
        
    
    def subtractDictValues(self,a,b):
        return dict( [ (n, a.get(n, 0) - b.get(n, 0)) for n in set(a)|set(b) ] ) #thank you stackoverflow!
