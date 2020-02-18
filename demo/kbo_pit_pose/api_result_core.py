import pickle
import time
import random


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

    def get_pit_pose_data(self, req):
        result = self.success_result

        try:
            pit_no = req.args.get('pit_no', type=str)
            data_all = None
            df_predict_result = None
            df_table = None

            with open('demo/kbo_pit_pose/data/pitch_predict_data_predict_result.pickle', 'rb') as f:
                data_all = pickle.load(f)

            if data_all is not None:
                df_predict_result = data_all[data_all.key == pit_no]

            if df_predict_result is not None and len(df_predict_result) > 0:
                with open('demo/kbo_pit_pose/data/pitch_predict_data_table.pickle', 'rb') as f:
                    data_all = pickle.load(f)

                if data_all is not None:
                    df_table = data_all[data_all.key == pit_no]

                if df_table is not None and len(df_table) > 0:
                    result['pit_predict'] = {
                        '직구확률': df_predict_result['직구'].values[0],
                        '변화구확률': df_predict_result['슬라이더'].values[0],
                        '실제구종': '변화구' if df_predict_result['pitch'].values[0] == '슬라이더'
                                        else df_predict_result['pitch'].values[0]
                    }

                    del df_table['pitch']
                    del df_table['key']

                    table_header = []
                    table_rows = []
                    for i, row in df_table.iterrows():
                        if i == 0:
                            table_header = list(row.index)

                        table_rows.append(list(row.values))

                    result['pose_data_table'] = {
                        'table_header': table_header,
                        'rows': table_rows
                    }

                    time.sleep(random.randrange(1,3))

                else:
                    result = self.no_data_result

            else:
                result = self.no_data_result

        except Exception as e:
            result = self.failure_result
            result['result_msg'] = str(e)

        return result