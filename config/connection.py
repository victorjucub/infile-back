import psycopg

class DBConnection:
    def __init__(self):
        try:
            self.conn = psycopg.connect(
                "dbname=infile user=postgres password=admin host=localhost port=5432"
            )
        except psycopg.OperationalError as err:
            print("[DBConnection] Error al conectar:", err)
            self.conn = None

    def get_cursor(self, row_factory=None):
        """Retorna un cursor con opcional row_factory"""
        if not self.conn:
            raise ConnectionError("No hay conexión a la base de datos")
        return self.conn.cursor(row_factory=row_factory)

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()