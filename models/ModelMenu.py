from .entities.User import User


class ModelMenu():
    @classmethod
    def earnings(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Liq_ganancias
            FROM operationhis 
            WHERE cc = {0}""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        list_result = [list(i) for i in result]
        liqTotal = 0
        print(list_result)
        for i in range(0, len(list_result)):
            liqTotal += list_result[i][0]
        return liqTotal