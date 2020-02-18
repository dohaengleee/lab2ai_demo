import config as c
from helper.sql_helper import SqlHelper

host = c.DB_CONFIG['host']
port = c.DB_CONFIG['port']
db = c.DB_CONFIG['db_name']
user = c.DB_CONFIG['user']
password = c.DB_CONFIG['password']
charset = c.DB_CONFIG['charset']


class GetDB:

    def __init__(self):
        self.sql_helper = SqlHelper(host, port, db, user, password, charset)

    def hitter(self, years):
        years_list = []
        if type(years) is list:
            for year in years:
                years_list.append("gmkey LIKE '{year}%' OR ".format(year=year))
            year_condition = ''.join(years_list)
            year_condition = year_condition[0:-4]
        else:
            year_condition = "gmkey LIKE '{year}%'".format(year=years)
        return self.sql_helper.call_db("""SELECT * FROM hitter WHERE {}""".format(year_condition))

    def pitcher(self, years):
        years_list = []
        if type(years) is list:
            for year in years:
                years_list.append("gday LIKE '{year}%' OR ".format(year=year))
            year_condition = ''.join(years_list)
            year_condition = year_condition[0:-4]
        else:
            year_condition = "gday LIKE '{year}%'".format(year=years)
        return self.sql_helper.call_db("""SELECT * FROM pitcher WHERE {}""".format(year_condition))

    def teamrank_daily(self, years):
        years_list = []
        if type(years) is list:
            for year in years:
                years_list.append("gyear LIKE '{year}%' OR ".format(year=year))
            year_condition = ''.join(years_list)
            year_condition = year_condition[0:-4]
        else:
            year_condition = "gyear LIKE '{year}%'".format(year=years)
        return self.sql_helper.call_db("""SELECT * FROM teamrank_daily WHERE {}""".format(year_condition))

    def entry(self, years):
        years_list = []
        if type(years) is list:
            for year in years:
                years_list.append("gyear LIKE '{year}%' OR ".format(year=year))
            year_condition = ''.join(years_list)
            year_condition = year_condition[0:-4]
        else:
            year_condition = "gyear LIKE '{year}%'".format(year=years)
        return self.sql_helper.call_db("""SELECT * FROM entry WHERE {}""".format(year_condition))

    def score(self, gmkey):
        return self.sql_helper.call_db("""SELECT * FROM score WHERE gmkey LIKE '{}'""".format(gmkey))

    def gameinfo(self, year=None, month=None, hteam=None, ateam=None, gmkey=None):
        if gmkey is not None:
            return self.sql_helper.call_db("""
                            SELECT * FROM gameinfo WHERE Gmkey = '{gmkey}'
                            """.format(gmkey=gmkey))

        if year and month and hteam and ateam is not None:
            return self.sql_helper.call_db("""
                SELECT * FROM
                (SELECT DISTINCT GmKey FROM gameinfo WHERE GmKey LIKE '{0}{1}%') AS A
                WHERE SUBSTRING(GmKey, 9, 2) = '{2}' AND SUBSTRING(GmKey, 11, 2) = '{3}'
                """.format(str(year), str(month), ateam, hteam))
        elif year and month and hteam is not None:
            return self.sql_helper.call_db("""
            SELECT * FROM
            (SELECT DISTINCT GmKey FROM gameinfo WHERE GmKey LIKE '{0}{1}%') AS A
            WHERE SUBSTRING(GmKey, 11, 2) = '{2}'
            """.format(str(year), str(month), hteam))
        elif year and month and ateam is not None:
            return self.sql_helper.call_db("""
            SELECT * FROM
            (SELECT DISTINCT GmKey FROM gameinfo WHERE GmKey LIKE '{0}{1}%') AS A
            WHERE SUBSTRING(GmKey, 9, 2) = '{2}'
            """.format(str(year), str(month), ateam))
        elif year and month is not None:
            return self.sql_helper.call_db("""
            SELECT DISTINCT GmKey FROM gameinfo WHERE GmKey like '{}%'""".format(str(year)+str(month)))
        elif year is not None:
            return self.sql_helper.call_db("""
            SELECT DISTINCT GmKey FROM gameinfo WHERE GmKey like '{}%' and SUBSTR(GMKEY, 5, 2) > '03';""".format(year))

    def gameinfo_all(self):
        return self.sql_helper.call_db("SELECT * FROM gameinfo;")

    def team_name(self):
        return self.sql_helper.call_db("SELECT team, team_kor FROM team_name;")

    def hitter_by_gmkey(self, gmkey):
        return self.sql_helper.call_db("SELECT * FROM hitter WHERE GMKEY='{gmkey}';".format(gmkey=gmkey))

    def person_all(self):
        return self.sql_helper.call_db("SELECT * FROM person;")

    def entry_by_gmkey(self, gmkey):
        return self.sql_helper.call_db("SELECT * FROM entry WHERE GMKEY='{gmkey}';".format(gmkey=gmkey))

