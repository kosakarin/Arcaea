import sqlite3, os
SQL = os.path.expanduser('~/.hoshino/arcaea.db')

class arcsql():
    def __init__(self):
        os.makedirs(os.path.dirname(SQL), exist_ok=True)
        self.makesql()
    
    def conn(self):
        return sqlite3.connect(SQL)

    def makesql(self):
        try:
            self.conn().execute('''CREATE TABLE USER(
                ID          INTEGER     PRIMARY KEY     NOT NULL,
                QQID        INTEGER     NOT NULL,
                ARCID       INTEGER     NOT NULL,
                ARCNAME     TEXT        NOT NULL
            )''')
        except Exception as e:
            print(e)
    
    def insert_user(self, qqid, arcid, arcname):
        try:
            conn = self.conn()
            conn.execute(f'INSERT INTO USER VALUES (NULL, {qqid}, {arcid}, "{arcname}")')
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_id(self, qqid):
        try:
            result = self.conn().execute(f'SELECT ARCID FROM USER WHERE QQID = {qqid}').fetchall()
            return result
        except Exception as e:
            print(e)
            return False

    def get_user_name(self, qqid):
        try:
            result = self.conn().execute(f'SELECT ARCNAME FROM USER WHERE QQID = {qqid}').fetchall()
            return result
        except Exception as e:
            print(e)
            return False
    
    def get_user_all(self, arcid):
        try:
            result = self.conn().execute(f'SELECT ARCID, ARCNAME FROM USER WHERE ARCID = {arcid}').fetchall()
            return result
        except Exception as e:
            print(e)
            return False
    
    def delete_user(self, qqid):
        try:
            conn = self.conn()
            conn.execute(f'DELETE FROM USER WHERE QQID = {qqid}')
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
