from .entities.User import User


class ModelTransactions():
    @classmethod
    def transactions(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Fecha_transaccion, Pago_cuota
            FROM operationhis 
            WHERE cc = {0} and Pago_cuota > 0
            ORDER BY Fecha_transaccion DESC""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        list_transactions = [list(i) for i in result]
        list_transactions = [x + ['Pago de cuota'] for x in list_transactions]
        list_transactions = [x + ['-'] for x in list_transactions]
        return list_transactions

    @classmethod
    def transactionsIntereses(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Fecha_transaccion, Pago_intereses
            FROM operationhis 
            WHERE cc = {0} and Pago_intereses > 0
            ORDER BY Fecha_transaccion DESC""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        list_transactions = [list(i) for i in result]
        list_transactions = [x + ['Pago de intereses'] for x in list_transactions]
        list_transactions = [x + ['-'] for x in list_transactions]
        return list_transactions
    
    @classmethod
    def transactionsStocks(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Fecha_transaccion, N_acciones_adq
            FROM operationhis 
            WHERE cc = {0} and N_acciones_adq > 0
            ORDER BY Fecha_transaccion DESC""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        list_transactions = [list(i) for i in result]
        list_transactions = [x + ['Compra de Acciones'] for x in list_transactions]
        list_transactions = [x + ['-'] for x in list_transactions]
        for i in range(0, len(list_transactions)):
            list_transactions[i][1] = list_transactions[i][1] * 10000
        return list_transactions

    @classmethod
    def transactionsLiqGa(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Fecha_transaccion, Liq_ganancias
            FROM operationhis 
            WHERE cc = {0} and Liq_ganancias > 0
            ORDER BY Fecha_transaccion DESC""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        list_transactions = [list(i) for i in result]
        list_transactions = [x + ['Liquidacion Ganancias'] for x in list_transactions]
        list_transactions = [x + ['+'] for x in list_transactions]
        return list_transactions