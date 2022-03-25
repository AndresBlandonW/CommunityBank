
from flask_login import current_user


class ModelInserts():

    @classmethod
    def InsertStock(self, cc, db, dateF, acts):
        cur = db.connection.cursor()
        sql = """INSERT INTO operationhis (cc, Nombre, Fecha_transaccion, N_acciones_adq, Pago_cuota, Pago_intereses, Credito_otorgado, Liq_ganancias)
        VALUES ({0}, 'Usuario', '{1}', {2}, 0, 0, 0, 0)
        """.format(cc, dateF, acts)
        cur.execute(sql)
        db.connection.commit()

    @classmethod
    def InsertStockStatus(self, cc, db, acts):
        cur = db.connection.cursor()
        sql = """SELECT N_acciones FROM statuspart WHERE cc = '{0}'""".format(cc)
        cur.execute(sql)
        row = cur.fetchone()
        newStocks = int(row[0]) + int(acts)
        cur = db.connection.cursor()
        sql = """UPDATE statuspart SET N_acciones = '{1}' WHERE cc = '{0}'""".format(cc, newStocks)
        cur.execute(sql)
        db.connection.commit()
    
    @classmethod
    def InsertStockhis(self, cc, db, dateF, acts):
        cur = db.connection.cursor()
        sql = """INSERT INTO stockhis (cc, fecha_compra, cantidad)
        VALUES ('{0}', '{1}', '{2}')
        """.format(cc, dateF, acts)
        cur.execute(sql)
        db.connection.commit()



    
    @classmethod
    def InsertCredit(self, cc, db, dateF, vCredito, cuotas, vCuotas, intereses):
        nombre = 'Usuario'
        cur = db.connection.cursor()
        sql = """INSERT INTO credithis (cc, Nombre, Fecha_credito, Valor_credito, Cuotas_credito, Valor_cuota, Interes_prestamo)
        VALUES ('{0}', '{1}', '{2}', {3}, {4}, {5}, {6})
        """.format(cc, nombre, dateF, vCredito, cuotas, vCuotas, intereses)
        cur.execute(sql)
        db.connection.commit()
    
    @classmethod
    def InsertCreditOperation(self, cc, db, dateF, vCredito):
        cur = db.connection.cursor()
        sql = """INSERT INTO operationhis (cc, Nombre, Fecha_transaccion, N_acciones_adq, Pago_cuota, Pago_intereses, Credito_otorgado, Liq_ganancias)
        VALUES ({0}, 'Usuario', '{1}', 0, 0, 0, {2}, 0)
        """.format(cc, dateF, vCredito)
        cur.execute(sql)
        db.connection.commit()

    
    @classmethod
    def InsertStatusPart(self, cc, db, vCredito, cuotas, vCuotas):
        cur = db.connection.cursor()
        sql = """SELECT Total_deuda_act FROM statuspart WHERE cc = '{0}'""".format(cc)
        cur.execute(sql)
        row = cur.fetchone()
        newCredit = int(row[0]) + int(vCredito)
        cur = db.connection.cursor()
        sql = """UPDATE statuspart SET Total_deuda_act = '{1}', Cuotas_pagar = '{2}', Valor_cuota = '{3}' WHERE cc = '{0}'""".format(cc, newCredit, cuotas, vCuotas)
        cur.execute(sql)
        db.connection.commit()