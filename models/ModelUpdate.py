

class ModelUpdate():

    @classmethod
    def update(self, cc, db, fullname, phone, email):
        cur = db.connection.cursor()
        sql = """UPDATE partner
            SET Nombre = '{0}',
                Email = '{1}',
                Telefono = '{2}'
            WHERE cc = {3}""".format(fullname, email, phone, cc)
        cur.execute(sql)
        db.connection.commit()

