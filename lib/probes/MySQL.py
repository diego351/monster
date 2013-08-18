import MySQLdb

class MySQL(object):

    def __init__(self,username, password):
        self.conn=MySQLdb.connect(host="localhost",user=username,passwd=password)
        self.cursor = self.conn.cursor()

    def report(self):
        self.cursor.execute("SHOW GLOBAL STATUS")
        returnDict = {}
        for row in self.cursor.fetchall():
            returnDict[row[0]] = row[1] #shut up and take data!
        return returnDict
        
