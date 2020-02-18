import pandas as pd
from demo.kbo_pitch_type import globals as g
from demo.kbo_pitch_type.db import GetDB
from xgboost import XGBClassifier


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

            df_schedule = g.DF_GAME_INFO_ALL[g.DF_GAME_INFO_ALL.gday.str.startswith(str(year))]

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

    def get_game_ts_pit_by_gmkey(self, req):
        result = self.success_result

        try:
            gmkey = req.args.get('gmkey', type=str)

            df_game_ts_pit = GetDB().stats_game_ts_pit_by_gmkey(gmkey)

            pitcher_list = req.args.get('pitcher_list', type=str)

            if pitcher_list is not None:
                pitcher_list = pitcher_list.split(',')
                df_game_ts_pit = df_game_ts_pit[df_game_ts_pit.pit_p_id.isin(pitcher_list)]

            pit_list = []
            if df_game_ts_pit.empty:
                result = self.no_data_result
                result['result_msg'] = '공 정보 없음'
            else:

                df_person = g.DF_PERSON
                df_person = df_person[(df_person.pcode != 'P0082') & (df_person.pcode != 'P0238') &
                                      (df_person.pcode != 'P0320') & (df_person.pcode != 'P0437')]
                df_person = df_person[['pcode', 'gyear', 'hittype']]
                df_person = df_person.astype({'pcode': int})
                df_game_ts_pit = pd.merge(df_game_ts_pit, df_person,
                                     left_on=['bat_p_id', 'season_id'], right_on=['pcode', 'gyear'], how='left')
                df_game_ts_pit['bat_hand_type'] = df_game_ts_pit.hittype.apply(lambda x: x[-2])
                df_game_ts_pit['bat_hand_type_cd'] = df_game_ts_pit.bat_hand_type.apply(lambda x: 0 if x == '좌' else 1 if x == '우' else 2)


                for i, row in df_game_ts_pit.iterrows():
                    pit = dict()
                    pit['le_id'] = row['le_id']
                    pit['sr_id'] = row['sr_id']
                    pit['g_id'] = row['g_id']
                    pit['pit_id'] = row['pit_id']
                    pit['season_id'] = row['season_id']
                    pit['inn_no'] = row['inn_no']
                    pit['bat_around_no'] = row['bat_around_no']
                    pit['tb_sc'] = row['tb_sc']
                    pit['t_id'] = row['t_id']
                    pit['bat_p_id'] = row['bat_p_id']
                    pit['bat_p_nm'] = g.get_player_name(row['season_id'], row['bat_p_id'])
                    pit['bat_order_no'] = row['bat_order_no']
                    pit['bat_pa_no'] = row['bat_pa_no']
                    pit['pit_p_id'] = row['pit_p_id']
                    pit['pit_p_nm'] = g.get_player_name(row['season_id'], row['pit_p_id'])
                    pit['pit_no'] = row['pit_no']
                    pit['pa_pit_no'] = row['pa_pit_no']
                    pit['pit_kind_cd'] = row['pit_kind_cd']
                    pit['get_pit_kind_name'] = g.get_pit_kind_name(row['pit_kind_cd'])
                    pit['pit_result_sc'] = row['pit_result_sc']
                    pit['pit_course_sc'] = row['pit_course_sc']
                    # pit['pit_course_no'] = row['pit_course_no'] # test
                    pit['pit_start_speed_va'] = row['pit_start_speed_va']
                    pit['cat_p_id'] = row['cat_p_id']
                    pit['cat_p_nm'] = g.get_player_name(row['season_id'], row['cat_p_id'])
                    pit['how_id'] = row['how_id']
                    pit['field_if'] = row['field_if']
                    pit['place_sc'] = row['place_sc']
                    pit['before_strike_cn'] = row['before_strike_cn']
                    pit['before_ball_cn'] = row['before_ball_cn']
                    pit['out_cn'] = row['out_cn']
                    pit['away_score_cn'] = row['away_score_cn']
                    pit['home_score_cn'] = row['home_score_cn']
                    pit['before_runner_cn'] = row['before_runner_cn']
                    pit['before_runner_sc'] = row['before_runner_sc']
                    pit['pit_count'] = row['pit_count']

                    pit['score_gap_group'] = row['score_gap_group']
                    pit['score_gap_group_cd'] = row['score_gap_group_cd']
                    pit['bat_order_group'] = row['bat_order_group']
                    pit['bat_order_group_cd'] = row['bat_order_group_cd']
                    pit['inn_no_group'] = row['inn_no_group']
                    pit['inn_no_group_cd'] = row['inn_no_group_cd']
                    pit['pit_count_group'] = row['pit_count_group']
                    pit['pit_count_group_cd'] = row['pit_count_group_cd']
                    pit['before_runner_sc_group'] = row['before_runner_sc_group']
                    pit['before_runner_sc_group_cd'] = row['before_runner_sc_group_cd']
                    pit['ballcount_group'] = row['ballcount_group']
                    pit['ballcount_group_cd'] = row['ballcount_group_cd']

                    pit['bat_hand_type'] = row['bat_hand_type']
                    pit['bat_hand_type_cd'] = row['bat_hand_type_cd']

                    pit_list.append(pit)

            result['pit_list'] = pit_list

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result

    def get_game_ts_pitcher_by_gmkey(self, req):
        result = self.success_result

        try:
            gmkey = req.args.get('gmkey', type=str)

            df_game_ts_pit = GetDB().stats_game_ts_pitcher_by_gmkey(gmkey)

            pitcher_list = []
            if df_game_ts_pit.empty:
                result = self.no_data_result
                result['result_msg'] = '선수 정보 없음'
            else:
                for i, row in df_game_ts_pit.iterrows():
                    pitcher = dict()
                    pitcher['index'] = i
                    pitcher['p_id'] = row['pit_p_id']
                    pitcher['pname'] = row['name']
                    pitcher['tname'] = row['team']
                    pitcher['seasonId'] = row['season_id']
                    pitcher['backnum'] = row['backnum']
                    pitcher['isChecked'] = True
                    pitcher_list.append(pitcher)

            result['pitcher_list'] = pitcher_list

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result

    def get_game_ts_pit_by_pitcher_all(self, req):
        result = self.success_result

        try:
            pit_p_id = req.args.get('pit_p_id', type=int)
            g_id = req.args.get('gmkey', type=str)
            pit_id = req.args.get('pit_id', type=str)

            df_ts_pit = GetDB().stats_game_ts_pit_pitcher_all(pit_p_id=pit_p_id, gmkey=g_id, pit_id=pit_id)

            if df_ts_pit.empty:
                result = self.no_data_result
                result['result_msg'] = '공 정보 없음'
            else:
                df_person = g.DF_PERSON
                df_person = df_person[(df_person.pcode != 'P0082') & (df_person.pcode != 'P0238') &
                                      (df_person.pcode != 'P0320') & (df_person.pcode != 'P0437')]
                df_person = df_person[['pcode', 'gyear', 'hittype']]
                df_person = df_person.astype({'pcode': int})
                df_ts_pit = pd.merge(df_ts_pit, df_person,
                                     left_on=['bat_p_id', 'season_id'], right_on=['pcode', 'gyear'], how='left')
                df_ts_pit['bat_hand_type'] = df_ts_pit.hittype.apply(lambda x: x[-2])
                df_ts_pit['bat_hand_type_cd'] = df_ts_pit.bat_hand_type.apply(lambda x: 0 if x == '좌' else 1 if x == '우' else 2)


                df_ts_pit_now = df_ts_pit[df_ts_pit.pit_id == pit_id]
                df_ts_pit_prev = df_ts_pit[df_ts_pit.pit_id < pit_id]

                now_info = dict()
                result['now_info'] = now_info

                now_game_situation = dict()
                now_game_situation['inn_no'] = df_ts_pit_now.inn_no.values[0]
                now_game_situation['bat_order_no'] = df_ts_pit_now.bat_order_no.values[0]
                now_game_situation['out_cn'] = df_ts_pit_now.out_cn.values[0]
                now_game_situation['before_runner_sc'] = df_ts_pit_now.before_runner_sc.values[0]
                now_game_situation['before_ball_cn'] = df_ts_pit_now.before_ball_cn.values[0]
                now_game_situation['before_strike_cn'] = df_ts_pit_now.before_strike_cn.values[0]
                now_game_situation['away_score_cn'] = df_ts_pit_now.away_score_cn.values[0]
                now_game_situation['home_score_cn'] = df_ts_pit_now.home_score_cn.values[0]
                now_game_situation['pit_count'] = df_ts_pit_now.pit_count.values[0]
                now_game_situation['bat_hand_type'] = df_ts_pit_now.bat_hand_type.values[0]
                now_info['now_game_situation'] = now_game_situation

                now_pitcher_situation_list = list()
                #check_group_list = ['inn_no_group', 'bat_order_group', 'out_cn', 'before_runner_sc_group', 'ballcount_group', 'score_gap_group', 'pit_count_group']
                check_group_list = ['ballcount_group', 'bat_hand_type', 'before_runner_sc_group', 'bat_order_group', 'out_cn',
                                    'score_gap_group', 'pit_count_group', 'inn_no_group']

                df_temp_for_pit_kind = None
                for group_name in check_group_list:
                    if len(df_ts_pit_prev[df_ts_pit_prev[group_name] == df_ts_pit_now[group_name].values[0]]) > 0:
                        now_value = df_ts_pit_now[group_name].values[0]

                        if df_temp_for_pit_kind is None:
                            df_temp_for_pit_kind = df_ts_pit_prev[df_ts_pit_prev[group_name] == now_value]
                        else:
                            df_temp_for_pit_kind = pd.concat([df_temp_for_pit_kind,
                                                             df_ts_pit_prev[df_ts_pit_prev[group_name] == now_value]])

                        now_pitcher_situation_list.append({
                            'group_name': group_name,
                            'is_record': True,
                            'group_value': now_value
                        })
                    else:
                        now_pitcher_situation_list.append({
                            'group_name': group_name,
                            'is_record': False
                        })

                if df_temp_for_pit_kind is not None:
                    now_info['now_pitcher_situation_check'] = True
                    now_info['now_pitcher_situation_list'] = now_pitcher_situation_list
                    print('이전 상황 기록 있음 {} row'.format(len(df_temp_for_pit_kind)))

                    df_temp_for_pit_kind = df_temp_for_pit_kind.drop_duplicates()

                    ser_situation_pit = df_temp_for_pit_kind.groupby('pit_kind_cd').count().le_id
                    ser_situation_pit = ser_situation_pit.sort_values(ascending=False)
                    situation_obj = dict()
                    situation_obj['pit_cnt'] = int(ser_situation_pit.values.sum())
                    situation_pit_list = list()
                    for key, value in ser_situation_pit.items():
                        sub_obj = {
                            'pit_code': key,
                            'pit_name': g.get_pit_kind_name(key),
                            'pit_cnt': int(value),
                            'pit_rate': 0.0 if int(ser_situation_pit.values.sum()) == 0 else value / ser_situation_pit.values.sum()
                        }
                        situation_pit_list.append(sub_obj)

                    now_info['situation_pit_kind_list'] = situation_pit_list

                else:
                    now_info['now_pitcher_situation_check'] = False
                    now_info['now_pitcher_situation_list'] = now_pitcher_situation_list
                    now_info['situation_pit_kind_list'] = []
                    print('이전 상황 기록 없음')

                now_info['real_pit_kind'] = {
                    'pit_code': df_ts_pit_now.pit_kind_cd.values[0],
                    'pit_name': g.get_pit_kind_name(df_ts_pit_now.pit_kind_cd.values[0])
                }

                series_all_pit_cd = pd.Series(
                    [0 for i in range(len(g.DF_CD_DETAIL.cd_se))], index=g.DF_CD_DETAIL.cd_se.to_list())

                ser_all_pit = df_ts_pit_prev.groupby('pit_kind_cd').count().le_id
                ser_all_pit = series_all_pit_cd.add(ser_all_pit, fill_value=0)
                obj = dict()
                obj['pit_cnt'] = int(ser_all_pit.values.sum())
                pit_list = list()
                for key, value in ser_all_pit.items():
                    sub_obj = {
                        'pit_code': key,
                        'pit_name': g.get_pit_kind_name(key),
                        'pit_cnt': int(value),
                        'pit_rate': 0.0 if int(ser_all_pit.values.sum()) == 0 else value / ser_all_pit.values.sum()
                    }
                    pit_list.append(sub_obj)

                obj['pit_kind_list'] = pit_list
                result['total_obj'] = obj

                sub_result = list()
                sub_result_detail = list()
                result['situation_list'] = sub_result
                result['situation_detail_list'] = sub_result_detail

                def get_pit_kind_list(situation_name=None, condition_list=None, column_name=None):
                    result_list = list()
                    for condition in condition_list:

                        if situation_name == '볼카운트별상세':
                            data_frame_temp = df_ts_pit_prev[(df_ts_pit_prev.before_ball_cn == condition['ball']) &
                                                             (df_ts_pit_prev.before_strike_cn == condition['strike'])]
                        else:
                            data_frame_temp = df_ts_pit_prev[df_ts_pit_prev[column_name] == condition]

                        series_pit = data_frame_temp.groupby('pit_kind_cd').count().le_id
                        series_pit = series_all_pit_cd.add(series_pit, fill_value=0)
                        result_obj = dict()

                        if situation_name == '볼카운트별상세':
                            result_obj['situation_detail'] = '{}-{}'.format(condition['ball'], condition['strike'])
                        else:
                            result_obj['situation_detail'] = condition

                        result_obj['pit_cnt'] = int(series_pit.values.sum())
                        pitch_list = list()
                        for k, v in series_pit.items():
                            pitch_list.append(
                                {
                                    'pit_code': k,
                                    'pit_name': g.get_pit_kind_name(k),
                                    'pit_cnt': int(v),
                                    'pit_rate': 0.0 if int(series_pit.values.sum()) == 0 else
                                    v / series_pit.values.sum()
                                }
                            )
                        result_obj['pit_kind_list'] = pitch_list
                        result_list.append(result_obj)

                    return result_list

                sub_result_detail.append({
                        'situation': '주자상황별',
                        'list': get_pit_kind_list(situation_name="주자상황상세",
                                                  condition_list=[0, 1, 2, 3, 12, 13, 23, 123],
                                                  column_name='before_runner_sc')})

                sub_result.append({
                    'situation': '주자상황별',
                    'list': get_pit_kind_list(situation_name="주자상황별",
                                              condition_list=['주자없음', '주자있음', '득점권'],
                                              column_name='before_runner_sc_group')})

                sub_result_detail.append({
                        'situation': '볼카운트별',
                        'list': get_pit_kind_list(situation_name="볼카운트별상세",
                                                  condition_list=[
                                                      {'ball': 0, 'strike': 0}, {'ball': 1, 'strike': 0},
                                                      {'ball': 2, 'strike': 0}, {'ball': 3, 'strike': 0},
                                                      {'ball': 0, 'strike': 1}, {'ball': 1, 'strike': 1},
                                                      {'ball': 2, 'strike': 1}, {'ball': 3, 'strike': 1},
                                                      {'ball': 0, 'strike': 2}, {'ball': 1, 'strike': 2},
                                                      {'ball': 2, 'strike': 2}, {'ball': 3, 'strike': 2}
                                                  ])})

                sub_result.append({
                    'situation': '볼카운트별',
                    'list': get_pit_kind_list(situation_name="볼카운트별",
                                              condition_list=['0-0', '유리', '불리'],
                                              column_name='ballcount_group')})

                sub_result_detail.append({
                        'situation': '아웃카운트별',
                        'list': get_pit_kind_list(situation_name="아웃카운트별",
                                                  condition_list=[0, 1, 2],
                                                  # condition_list=[0, 1, 2, 4],
                                                  column_name='out_cn')})

                sub_result.append({
                    'situation': '아웃카운트별',
                    'list': get_pit_kind_list(situation_name="아웃카운트별",
                                              condition_list=[0, 1, 2],
                                              # condition_list=[0, 1, 2, 4],
                                              column_name='out_cn')})

                sub_result_detail.append({
                        'situation': '타순별',
                        'list': get_pit_kind_list(situation_name="타순별",
                                                  condition_list=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                                                  column_name='bat_order_no')})

                sub_result.append({
                        'situation': '타순별',
                        'list': get_pit_kind_list(situation_name="타순별",
                                                  condition_list=['테이블세터', '클린업트리오', '하위타선'],
                                                  column_name='bat_order_group')})

                sub_result_detail.append({
                        'situation': '이닝별',
                        'list': get_pit_kind_list(situation_name="이닝별",
                                                  condition_list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                                  column_name='inn_no')})

                sub_result.append({
                        'situation': '이닝별',
                        'list': get_pit_kind_list(situation_name="이닝구분별",
                                                  condition_list=['1~3', '4~6', '7~9', '연장'],
                                                  column_name='inn_no_group')})

                sub_result_detail.append({
                    'situation': '점수차별',
                    'list': get_pit_kind_list(situation_name="점수차별",
                                              condition_list=['0D', '1~2W', '3~5W', '5W+', '1~2L', '3~5L', '5L+'],
                                              column_name='score_gap_group')})
                sub_result.append({
                    'situation': '점수차별',
                    'list': get_pit_kind_list(situation_name="점수차별",
                                              condition_list=['0D', '1~2W', '3~5W', '5W+', '1~2L', '3~5L', '5L+'],
                                              column_name='score_gap_group')})

                sub_result_detail.append({
                    'situation': '투구수별',
                    'list': get_pit_kind_list(situation_name="투구수별",
                                              condition_list=['0~20', '21~40', '41~60', '61~80', '81~100', '100~'],
                                              column_name='pit_count_group')})

                sub_result.append({
                        'situation': '투구수별',
                        'list': get_pit_kind_list(situation_name="투구수별",
                                                  condition_list=['0~20', '21~40', '41~60', '61~80', '81~100', '100~'],
                                                  column_name='pit_count_group')})

                sub_result_detail.append({
                    'situation': '타자유형별',
                    'list': get_pit_kind_list(situation_name="타자유형별",
                                              condition_list=['좌', '우', '양'],
                                              column_name='bat_hand_type')})

                sub_result.append({
                    'situation': '타자유형별',
                    'list': get_pit_kind_list(situation_name="타자유형별",
                                              condition_list=['좌', '우', '양'],
                                              column_name='bat_hand_type')})

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result

    def get_predict(self, req):
        result = self.success_result

        try:
            pit_p_id = req.args.get('pit_p_id', type=int)
            g_id = req.args.get('gmkey', type=str)
            pit_id = req.args.get('pit_id', type=str)

            df_ts_pit = GetDB().stats_game_ts_pit_pitcher_all(pit_p_id=pit_p_id, gmkey=g_id, pit_id=pit_id)
            df_person = g.DF_PERSON
            df_person = df_person[(df_person.pcode != 'P0082') & (df_person.pcode != 'P0238') &
                                  (df_person.pcode != 'P0320') & (df_person.pcode != 'P0437')]
            df_person = df_person[['pcode', 'gyear', 'hittype']]
            df_person = df_person.astype({'pcode': int})
            df_ts_pit = pd.merge(df_ts_pit, df_person,
                                 left_on=['bat_p_id', 'season_id'], right_on=['pcode', 'gyear'], how='left')
            df_ts_pit['bat_hand_type'] = df_ts_pit.hittype.apply(lambda x: x[-2])
            df_ts_pit['bat_hand_type_cd'] = df_ts_pit.bat_hand_type.apply(lambda x: 0 if x == '좌' else 1 if x == '우' else 2)

            if df_ts_pit.empty:
                result = self.no_data_result
                result['result_msg'] = '공 정보 없음'
            else:

                df_ts_pit = df_ts_pit.astype({'before_runner_sc_group_cd': int})
                df_ts_pit_now = df_ts_pit[df_ts_pit.pit_id == pit_id]
                df_ts_pit_prev = df_ts_pit[df_ts_pit.pit_id < pit_id]

                x_train = df_ts_pit_prev[
                    ['bat_p_id', 'before_ball_cn', 'before_strike_cn', 'inn_no', 'inn_no_group_cd', 'bat_order_no',
                     'bat_order_group_cd', 'out_cn', 'before_runner_sc_group_cd', 'ballcount_group_cd', 'pit_count',
                     'pit_no', 'score_gap_group_cd', 'pit_count_group_cd', 'bat_hand_type_cd', 'cat_p_id']]
                x_test = df_ts_pit_now[
                    ['bat_p_id', 'before_ball_cn', 'before_strike_cn', 'inn_no', 'inn_no_group_cd', 'bat_order_no',
                     'bat_order_group_cd', 'out_cn', 'before_runner_sc_group_cd', 'ballcount_group_cd', 'pit_count',
                     'pit_no', 'score_gap_group_cd', 'pit_count_group_cd', 'bat_hand_type_cd', 'cat_p_id']]
                y_train = df_ts_pit_prev['pit_kind_cd']

                model = XGBClassifier(objective='multi:softmax', num_class=len(y_train.unique()))
                model.fit(x_train, y_train)
                predict_prob = model.predict_proba(x_test)[0]
                ser_predict_prob = pd.Series(predict_prob, index=sorted(y_train.unique())).sort_values(ascending=False)

                dic_all_pit = dict()
                for k, v in ser_predict_prob.items():
                    dic_all_pit[k] = v

                #result['predict_prob'] = dic_all_pit
                predict_prob_list = []
                for key, value in dic_all_pit.items():
                    predict_prob_list.append({
                        'pit_cd': key,
                        'pit_nm': g.get_pit_kind_name(key),
                        'pit_rt': value
                    })
                result['predict_prob_list'] = predict_prob_list

                result['real_pitch'] = g.get_pit_kind_name(df_ts_pit_now.pit_kind_cd.values[0])


        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result