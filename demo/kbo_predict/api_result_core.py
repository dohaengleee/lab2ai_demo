from demo.kbo_predict.lib.tester import Tester, scheduler
from demo.kbo_predict import util as u
from demo.kbo_predict.lib.trainer import Trainer
import datetime
from demo.kbo_predict import globals as g
from demo.kbo_predict.db import GetDB


class ApiResultCore(object):

    def __init__(self):
        self.success_result = {
            'result_code': 100,
            'result_msg': '성공'
        }
        self.no_data_result = {
            'result_code': 200,
            'result_msg': '데이터 없음'
        }
        self.failure_result = {
            'result_code': 300,
            'result_msg': '실패'
        }

    def get_schedule(self, req):
        result = self.success_result

        try:
            year = req.args.get('year', type=int)
            month = req.args.get('month', type=int)
            hteam = req.args.get('hteam', type=str)
            ateam = req.args.get('ateam', type=str)
            if month is not None and month < 10:
                month = '0' + str(month)

            gmkey_list = list()
            #df_schedule = scheduler(year, month, hteam, ateam)

            df_schedule = g.DF_GAME_INFO_ALL[(g.DF_GAME_INFO_ALL.gday.str.startswith(str(year)))
                                             & (~g.DF_GAME_INFO_ALL.gday.str.contains('201903'))]

            if month is not None:
                df_schedule = df_schedule[df_schedule.gday.str.startswith(str(year) + str(month))]

            if ateam is not None:
                df_schedule = df_schedule[df_schedule.gmkey.str[8:10] == ateam]

            if hteam is not None:
                df_schedule = df_schedule[df_schedule.gmkey.str[10:12] == hteam]

            if df_schedule.empty:
                result = self.no_data_result
                result['result_msg'] = '해당 경기 없음'
            else:
                gmkey_list = list(df_schedule.to_dict()['gmkey'].values())

            result['gmkey'] = gmkey_list

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result

    def get_predict(self, req):
        result = self.success_result

        try:
            gmkey = req.args.get('gmkey', type=str)
            tester = Tester(gmkey, predict_game=True)
            predict_result = tester.predict().tolist()
            start_pitcher_info = tester.get_start_pitcher()
            if len(predict_result) > 0:

                df_game_info = g.DF_GAME_INFO_ALL[g.DF_GAME_INFO_ALL.gmkey == gmkey]
                stadium = ''
                if len(df_game_info) > 0:
                    stadium = df_game_info.stadium.values[0]

                dic_predict = dict()
                dic_predict['gmkey'] = gmkey
                dic_predict['g_dt'] = datetime.datetime.strptime(gmkey[0:8], '%Y%m%d').strftime('%Y.%m.%d')
                dic_predict['stadium'] = stadium
                dic_predict['a_t_cd'] = gmkey[8:10]
                dic_predict['h_t_cd'] = gmkey[10:12]
                dic_predict['a_t_nm'] = u.get_team_name(gmkey[8:10])
                dic_predict['h_t_nm'] = u.get_team_name(gmkey[10:12])
                dic_predict['a_win_rt'] = predict_result[0][0]
                dic_predict['h_win_rt'] = predict_result[0][1]

                result['predict_result'] = dic_predict
                result['real_result'] = Tester(gmkey).real_score()

                dic_pitcher_info = dict()
                dic_pitcher_info['a_pitcher'] = start_pitcher_info['a_pitcher']
                dic_pitcher_info['h_pitcher'] = start_pitcher_info['h_pitcher']
                dic_pitcher_info['a_pitcher_era'] = start_pitcher_info['a_pitcher_era']
                dic_pitcher_info['h_pitcher_era'] = start_pitcher_info['h_pitcher_era']
                result['real_result']['pitcher_info'] = dic_pitcher_info
            else:
                result = self.no_data_result

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result

    def get_hitrate_predict(self, req):
        result = self.success_result

        try:
            gmkey = req.args.get('gmkey', type=str)
            predict_result = Tester(gmkey, predict_game=False).predict_hitrate()
            if len(predict_result) > 0:
                result['gmkey'] = gmkey
                result['away'] = predict_result[0]
                result['home'] = predict_result[1]

                df_hitter = GetDB().hitter_by_gmkey(gmkey)
                df_entry = GetDB().entry_by_gmkey(gmkey)

                def add_info(list):
                    for val in list:
                        val['back_no'] = u.get_person_back_no(gmkey[:4], str(val['pcode']))
                        bat_order = ''
                        if len(df_entry[(df_entry.pcode == str(val['pcode']))].turn.values) > 0:
                            bat_order = df_entry[(df_entry.pcode == str(val['pcode']))].turn.values[0][-1:]
                        val['bat_order'] = bat_order

                        df_player = df_hitter[df_hitter.pcode == str(val['pcode'])]

                        if len(df_player) > 0:
                            val['pa'] = df_player.pa.values[0]
                            val['ab'] = df_player.ab.values[0]
                            val['hit'] = df_player.hit.values[0]
                            val['hr'] = df_player.hr.values[0]
                        else:
                            val['pa'] = ''
                            val['ab'] = ''
                            val['hit'] = ''
                            val['hr'] = ''

                add_info(predict_result[0]['hitter_list'])
                add_info(predict_result[1]['hitter_list'])
            else:
                result = self.no_data_result

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result

    def get_real_score(self, req):
        result = self.success_result

        try:
            gmkey = req.args.get('gmkey', type=str)
            result = Tester(gmkey).real_score()

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result

    def get_train(self, req):
        result = self.success_result

        try:
            start_year = req.args.get('start', type=int)
            end_year = req.args.get('end', type=int)
            if start_year and end_year is not None:
                years = [i for i in range(start_year, end_year + 1)]
            elif start_year is not None and end_year is None:
                years = start_year
            else:
                years = end_year
            trainer = Trainer(years)
            trainer.training()
            trainer.model_saver()
            result = trainer.model_score()

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result
