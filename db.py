import rethinkdb as r

def DBManager():

    def connect(self):
        self.cnx = r.connect(host="localhost", port=28015, db="pyBOT")



