from .entities.User import User


class ModelCred():

    @classmethod
    def ValueCre(self, cc, db):
        cur = db.connection.cursor()
        sql = """SELECT Fecha_credito, Valor_credito, Cuotas_credito, Valor_cuota, Interes_prestamo
            FROM credithis 
            WHERE cc = {0} and Valor_credito > 0
            ORDER BY Fecha_credito DESC""". format(cc)
        cur.execute(sql)
        result = cur.fetchall()
        list_credts = [list(i) for i in result]
        list_credts = [x + ['Valor credito'] for x in list_credts]
        list_credts = [x + ['-'] for x in list_credts]
        return list_credts
