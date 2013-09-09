class MySQL(object):

    def __init__(self, options):
        # Let's see if MySQLdb is present.
        # If not, we raise an exception with a slightly more
        # helpful message that the default ImportError
        try:
            import MySQLdb
        except ImportError:
            raise Exception(
                "You tried to load the MySQL probe, but the MySQLdb module\n"
                "does not seem to be present. Try installing with pip mysql-python\n"
                "(you may need a mysql-dev package on your system for that, by the way)\n"
            )

        self.conn = MySQLdb.connect(
            host="localhost", user=options.get('username'), passwd=options.get('password'))
        self.cursor = self.conn.cursor()
        self.firstTime = True
        self.emptyDict = {
            "delete": 0,
            "select": 0,
            "insert": 0,
            "update": 0,
            "connections": 0,
        }

    def report(self):
        if self.firstTime:
            self.myBuffer = self.getCurrentData()
            self.firstTime = False
            return self.emptyDict
        else:
            curr = self.getCurrentData()
            toRet = self.subtractDictValues(curr, self.myBuffer)
            self.myBuffer = curr
            return toRet

    def getCurrentData(self):
        self.cursor.execute("SHOW GLOBAL STATUS")
        temp = {}
        for row in self.cursor.fetchall():
            temp[row[0]] = row[1]

        return {
            "delete": int(temp["Com_delete"]),
            "select": int(temp["Com_select"]),
            "insert": int(temp["Com_insert"]),
            "update": int(temp["Com_update"]),
            "connections": int(temp["Connections"]),
        }

    def subtractDictValues(self, a, b):
        #thank you stackoverflow!
        return dict([(n, a.get(n, 0) - b.get(n, 0)) for n in set(a) | set(b)])
