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

    def stats_cd_detail(self):
        return self.sql_helper.call_db("SELECT * FROM stats_cd_detail WHERE CM_SE = 8;")

    def stats_game_ts_pit_by_gmkey(self, gmkey):
        return self.sql_helper.call_db("""
            SELECT LE_ID, SR_ID, G_ID, PIT_ID, SEASON_ID, INN_NO, BAT_AROUND_NO, TB_SC, T_ID
                , BAT_P_ID, BAT_ORDER_NO, BAT_PA_NO
                , PIT_P_ID, PIT_NO, PA_PIT_NO, PIT_KIND_CD, PIT_RESULT_SC, PIT_COURSE_SC, PIT_COURSE_NO, PIT_START_SPEED_VA
                , CAT_P_ID
                , HOW_ID, FIELD_IF, PLACE_SC, BEFORE_STRIKE_CN, BEFORE_BALL_CN, OUT_CN, AWAY_SCORE_CN, HOME_SCORE_CN, BEFORE_RUNNER_CN, BEFORE_RUNNER_SC
                , ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) AS PIT_COUNT
                , (CASE WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN '5W+'
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN '3~5W'
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN '1~2W'					 
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN '5L+'
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN '3~5L'
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN '1~2L'
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN '5L+'
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN '3~5L'
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN '1~2L'					 
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN '5W+'
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN '3~5W'
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN '1~2W'
                         ELSE '0D' END)
                    AS SCORE_GAP_GROUP
                , (CASE WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN 5
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN 3
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN 1
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN -5
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN -3
                         WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN -1
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN -5
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN -3
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN -1
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                             THEN 5
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                             THEN 3
                         WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                             THEN 1
                         ELSE 0 END)
                    AS SCORE_GAP_GROUP_CD
                , (CASE WHEN BAT_ORDER_NO IN (1,2) THEN '테이블세터'
                        WHEN BAT_ORDER_NO IN (3,4,5) THEN '클린업트리오'
                        ELSE '하위타선' END) AS BAT_ORDER_GROUP
                , (CASE WHEN BAT_ORDER_NO IN (1,2) THEN 1
                        WHEN BAT_ORDER_NO IN (3,4,5) THEN 2
                        ELSE 3 END) AS BAT_ORDER_GROUP_CD
                , (CASE WHEN INN_NO IN (1,2,3) THEN '1~3'
                        WHEN INN_NO IN (4,5,6) THEN '4~6'
                        WHEN INN_NO IN (7,8,9) THEN '7~9'
                        ELSE '연장' END) AS INN_NO_GROUP
                , (CASE WHEN INN_NO IN (1,2,3) THEN 1
                        WHEN INN_NO IN (4,5,6) THEN 4
                        WHEN INN_NO IN (7,8,9) THEN 7
                        ELSE 10 END) AS INN_NO_GROUP_CD
                , (CASE WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 20 THEN '0~20'
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 40 THEN '21~40'
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 60 THEN '41~60'
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 80 THEN '61~80'
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 100 THEN '81~100'
                      ELSE '100~'
                  END) AS PIT_COUNT_GROUP
                , (CASE WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 20 THEN 0
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 40 THEN 20
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 60 THEN 40
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 80 THEN 60
                      WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 100 THEN 80
                      ELSE 100
                  END) AS PIT_COUNT_GROUP_CD
               , (CASE WHEN BEFORE_RUNNER_SC = 0 THEN '주자없음'
                     WHEN BEFORE_RUNNER_SC = 1 THEN '주자있음'
                     ELSE '득점권'
                END) BEFORE_RUNNER_SC_GROUP
               , (CASE WHEN BEFORE_RUNNER_SC = 0 THEN '0'
                     WHEN BEFORE_RUNNER_SC = 1 THEN '1'
                     ELSE '2'
                END) BEFORE_RUNNER_SC_GROUP_CD
               , (CASE WHEN BEFORE_BALL_CN > BEFORE_STRIKE_CN THEN '불리'
                     WHEN BEFORE_BALL_CN = 0 AND BEFORE_STRIKE_CN = 0 THEN '0-0'
                     ELSE '유리'
                END) BALLCOUNT_GROUP
               , (CASE WHEN BEFORE_BALL_CN > BEFORE_STRIKE_CN THEN -1
                     WHEN BEFORE_BALL_CN = 0 AND BEFORE_STRIKE_CN = 0 THEN 0
                     ELSE 1
                END) BALLCOUNT_GROUP_CD
            FROM stats_game_ts_pit
            WHERE LE_ID = 1 AND SR_ID = 0 AND PIT_RESULT_SC IN ('T','B','S','F','V','W','H')
                AND G_ID = '{gmkey}'
            ORDER BY PIT_ID;
            """.format(gmkey=gmkey))

    def stats_game_ts_pitcher_by_gmkey(self, gmkey):
        return self.sql_helper.call_db("""
            SELECT SEASON_ID, PIT_P_ID, `NAME`, TEAM, BACKNUM
            FROM
            (
                SELECT SEASON_ID, PIT_P_ID, MIN(PIT_ID) AS PIT_ID
                FROM stats_game_ts_pit
                WHERE LE_ID = 1 AND SR_ID = 0 AND PIT_RESULT_SC IN ('T','B','S','F','V','W','H')
                    AND G_ID = '{gmkey}'
                GROUP BY SEASON_ID, PIT_P_ID
            ) AS A
            LEFT OUTER JOIN
            (
                SELECT GYEAR, PCODE, `NAME`, TEAM, BACKNUM FROM person
            ) AS B
            ON A.SEASON_ID = B.GYEAR AND A.PIT_P_ID = B.PCODE
            ORDER BY A.PIT_ID
            """.format(gmkey=gmkey))

    def stats_game_ts_pit_pitcher_all(self, pit_p_id, gmkey, pit_id):
        return self.sql_helper.call_db("""
               SELECT LE_ID, SR_ID, G_ID, PIT_ID, SEASON_ID, INN_NO, BAT_AROUND_NO, TB_SC, T_ID
                    , BAT_P_ID, BAT_ORDER_NO, BAT_PA_NO
                    , PIT_P_ID, PIT_NO, PA_PIT_NO, PIT_KIND_CD, PIT_RESULT_SC, PIT_COURSE_SC, PIT_COURSE_NO, PIT_START_SPEED_VA
                    , CAT_P_ID
                    , HOW_ID, FIELD_IF, PLACE_SC, BEFORE_STRIKE_CN, BEFORE_BALL_CN, OUT_CN, AWAY_SCORE_CN, HOME_SCORE_CN, BEFORE_RUNNER_CN, BEFORE_RUNNER_SC
                    , ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) AS PIT_COUNT
                    , (CASE WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN '5W+'
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN '3~5W'
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN '1~2W'					 
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN '5L+'
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN '3~5L'
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN '1~2L'
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN '5L+'
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN '3~5L'
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN '1~2L'					 
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN '5W+'
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN '3~5W'
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN '1~2W'
                             ELSE '0D' END)
                        AS SCORE_GAP_GROUP
                    , (CASE WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN 5
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN 3
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN 1
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN -5
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN -3
                             WHEN AWAY_SCORE_CN > HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN -1
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN -5
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN -3
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'B' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN -1
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 5
                                 THEN 5
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 2
                                 THEN 3
                             WHEN AWAY_SCORE_CN < HOME_SCORE_CN AND TB_SC = 'T' AND ABS(AWAY_SCORE_CN - HOME_SCORE_CN) > 0
                                 THEN 1
                             ELSE 0 END)
                        AS SCORE_GAP_GROUP_CD
                    , (CASE WHEN BAT_ORDER_NO IN (1,2) THEN '테이블세터'
                            WHEN BAT_ORDER_NO IN (3,4,5) THEN '클린업트리오'
                            ELSE '하위타선' END) AS BAT_ORDER_GROUP
                    , (CASE WHEN BAT_ORDER_NO IN (1,2) THEN 1
                            WHEN BAT_ORDER_NO IN (3,4,5) THEN 2
                            ELSE 3 END) AS BAT_ORDER_GROUP_CD
                    , (CASE WHEN INN_NO IN (1,2,3) THEN '1~3'
                            WHEN INN_NO IN (4,5,6) THEN '4~6'
                            WHEN INN_NO IN (7,8,9) THEN '7~9'
                            ELSE '연장' END) AS INN_NO_GROUP
                    , (CASE WHEN INN_NO IN (1,2,3) THEN 1
                            WHEN INN_NO IN (4,5,6) THEN 4
                            WHEN INN_NO IN (7,8,9) THEN 7
                            ELSE 10 END) AS INN_NO_GROUP_CD
                    , (CASE WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 20 THEN '0~20'
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 40 THEN '21~40'
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 60 THEN '41~60'
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 80 THEN '61~80'
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 100 THEN '81~100'
                          ELSE '100~'
                      END) AS PIT_COUNT_GROUP
                    , (CASE WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 20 THEN 0
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 40 THEN 20
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 60 THEN 40
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 80 THEN 60
                          WHEN ROW_NUMBER() OVER (PARTITION BY LE_ID, SR_ID, G_ID, PIT_P_ID ORDER BY PIT_NO ASC) < 100 THEN 80
                          ELSE 100
                      END) AS PIT_COUNT_GROUP_CD
                   , (CASE WHEN BEFORE_RUNNER_SC = 0 THEN '주자없음'
                         WHEN BEFORE_RUNNER_SC = 1 THEN '주자있음'
                         ELSE '득점권'
                    END) BEFORE_RUNNER_SC_GROUP
                   , (CASE WHEN BEFORE_RUNNER_SC = 0 THEN '0'
                         WHEN BEFORE_RUNNER_SC = 1 THEN '1'
                         ELSE '2'
                    END) BEFORE_RUNNER_SC_GROUP_CD
                   , (CASE WHEN BEFORE_BALL_CN > BEFORE_STRIKE_CN THEN '불리'
                         WHEN BEFORE_BALL_CN = 0 AND BEFORE_STRIKE_CN = 0 THEN '0-0'
                         ELSE '유리'
                    END) BALLCOUNT_GROUP
                   , (CASE WHEN BEFORE_BALL_CN > BEFORE_STRIKE_CN THEN -1
                         WHEN BEFORE_BALL_CN = 0 AND BEFORE_STRIKE_CN = 0 THEN 0
                         ELSE 1
                    END) BALLCOUNT_GROUP_CD
               FROM stats_game_ts_pit
               WHERE LE_ID = 1 AND SR_ID = 0 AND PIT_RESULT_SC IN ('T','B','S','F','V','W','H')
                    AND PIT_P_ID = {pit_p_id} AND G_ID <= '{gmkey}' AND PIT_ID <= '{pit_id}'
               ORDER BY G_ID, PIT_ID;
               """.format(pit_p_id=pit_p_id, gmkey=gmkey, pit_id=pit_id))