import pymysql
import pandas as pd


class SqlHelper:
    def __init__(self, host, port, db_name, user, password, charset):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password
        self.charset = charset

    def call_db(self, query):
        df = None
        conn = None
        try:
            # Open database connection
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db_name
                                   , charset=self.charset, autocommit=True, cursorclass=pymysql.cursors.DictCursor)
            cursor = conn.cursor()
            cursor.execute(query)

            result = cursor.fetchall()
            df = pd.DataFrame(result)
            df.columns = map(str.lower, df.columns)
        except Exception as e:
            print(e)
        finally:
            if conn is not None:
                # disconnect from server
                conn.close()

        return df

