from .entities.User import User


class ModelHome():
    
    @classmethod
    def ValueStoks(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Valor_acciones
            FROM statuspart 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        valueStocks = result[0][0]
        return valueStocks

## Total_deuda_act, Cuotas_pagar, Valor_cuota

    @classmethod
    def CreditActual(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Total_deuda_act
            FROM statuspart 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        creditAct = result[0][0]
        return creditAct

    @classmethod
    def PendCuot(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Cuotas_pagar
            FROM statuspart 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        pendCuot = result[0][0]
        return pendCuot

    @classmethod
    def ValueCuot(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Valor_cuota
            FROM statuspart 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        valueCuot = result[0][0]
        return valueCuot

    @classmethod
    def TotalStocks(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT N_acciones
            FROM statuspart 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        totalStocks = result[0][0]
        return totalStocks