import sqlite3, os
SQL = os.path.expanduser('~/.hoshino/arcaea.db')
SONGSQL = os.path.join(os.path.dirname(__file__), 'arcsong.db')

class arcsql():
    def __init__(self):
        os.makedirs(os.path.dirname(SQL), exist_ok=True)
        self.makesql()
    
    def arc_conn(self):
        return sqlite3.connect(SQL)

    def song_conn(self):
        return sqlite3.connect(SONGSQL)

    def makesql(self):
        try:
            self.arc_conn().execute('''CREATE TABLE USER(
                ID          INTEGER     PRIMARY KEY     NOT NULL,
                QQID        INTEGER     NOT NULL,
                ARCID       INTEGER     NOT NULL,
                ARCNAME     TEXT        NOT NULL,
                USER_ID     INTEGER,
                BIND_ID     INTEGER
            )''')
        except Exception as e:
            print(e)
    
    def makelogin(self):
        try:
            self.arc_conn().execute('''CREATE TABLE LOGIN(
                ID          INTEGER     PRIMARY KEY     NOT NULL,
                BIND_ID     INTEGER     NOT NULL,
                EMAIL       TEXT        NOT NULL,
                PASSWORD    TEXT        NOT NULL
            )''')
        except Exception as e:
            print(e)
    
    def insert_temp_user(self, qqid, arcid, arcname):
        try:
            conn = self.arc_conn()
            conn.execute(f'INSERT INTO USER VALUES (NULL, {qqid}, {arcid}, "{arcname.lower()}", NULL, NULL)')
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def insert_user(self, arcname, user_id, bind_id):
        try:
            conn = self.arc_conn()
            conn.execute(f'UPDATE USER SET ARCNAME = "{arcname}", USER_ID = {user_id}, BIND_ID = {bind_id} WHERE ARCNAME = "{arcname}"')
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_id(self, qqid):
        try:
            result = self.arc_conn().execute(f'SELECT USER_ID FROM USER WHERE QQID = {qqid}').fetchall()
            return result
        except Exception as e:
            print(e)
            return False

    def get_user_name(self, user_id):
        try:
            result = self.arc_conn().execute(f'SELECT ARCNAME FROM USER WHERE USER_ID = {user_id}').fetchall()
            return result
        except Exception as e:
            print(e)
            return False

    def get_bind_id(self, user_id):
        try:
            result = self.arc_conn().execute(f'SELECT ARCID, BIND_ID FROM USER WHERE USER_ID = {user_id}').fetchall()
            return result
        except Exception as e:
            print(e)
            return False

    def get_all_login(self):
        try:
            result = self.arc_conn().execute(f'SELECT BIND_ID, EMAIL, PASSWORD FROM LOGIN').fetchall()
            return result
        except Exception as e:
            print(e)
            return False
    
    def get_login(self, bind_id):
        try:
            result = self.arc_conn().execute(f'SELECT EMAIL, PASSWORD FROM LOGIN WHERE BIND_ID = {bind_id}').fetchall()
            return result
        except Exception as e:
            print(e)
            return False
    
    def delete_user(self, qqid):
        try:
            conn = self.arc_conn()
            conn.execute(f'DELETE FROM USER WHERE QQID = {qqid}')
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def song_info(self, sid, diff):
        try:
            result = self.song_conn().execute(f'select name_en, name_jp, artist, {diff}  from songs where sid = "{sid}"').fetchall()
            return result
        except Exception as e:
            print(e)
            return False
