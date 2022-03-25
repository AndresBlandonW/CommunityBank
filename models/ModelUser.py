from .entities.User import User


class ModelUser():
    
    @classmethod
    def login(self, db, user):
        cur = db.connection.cursor()
        sql = """SELECT cc, Password, Telefono, Nombre, Email
            FROM partner 
            WHERE cc = {0} and Password = '{1}'""".format(user.identity, user.password)
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            user_data = User(row[0], row[0], True, row[2], row[3], row[4])
            return user_data
        else:
            return None
    
    @classmethod
    def getphone(self, db, cc):
        cur = db.connection.cursor()
        sql = """SELECT Telefono
            FROM partner
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        row = cur.fetchone()
        return row[0]
    
    
    @classmethod
    def lockuser(self, db, cc):
        cur = db.connection.cursor()
        sql = """UPDATE partner 
            SET status = 2
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        return True

    @classmethod
    def get_data(self, db, id):
        cur = db.connection.cursor()
        sql = """SELECT cc, Telefono, Nombre, Email
            FROM partner 
            WHERE cc = {}""". format(id)
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return User(row[0], row[0], None, row[1], row[2], row[3])
        else:
            return None
    
    @classmethod
    def credit(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Cuotas_credito
            FROM credithis 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return None
    
    @classmethod
    def stocks(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT N_acciones_adq
            FROM operationhis 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return 0
