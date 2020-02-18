from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
# from lib.tester import Tester, scheduler
# from lib.trainer import Trainer
from helper.response_helper import ResponseHelper
from demo.kbo_predict.api_result_core import ApiResultCore as PredictResult
from demo.kbo_predict import globals as predict_g
from demo.kbo_pit_pose.api_result_core import ApiResultCore as PitPoseResult
from helper.log_helper import LogHelper

from demo.kbo_pitch_type.api_result_core import ApiResultCore as PitchTypeResult
from demo.kbo_pitch_type import globals as pitchtype_g



app = Flask(__name__)
CORS(app)
api = Api(app)


def get_ip():
    try:
        return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    except Exception as e:
        return ''


def set_access_log(msg):
    ip = get_ip()
    if len(ip) > 0:
        LogHelper.instance().i('{message} - ip: {ip}'.format(message=msg, ip=get_ip()))
    else:
        LogHelper.instance().i('{message}'.format(message=msg))


class Predict(Resource):

    def get(self):
        set_access_log('Predict-get')

        predict_result = PredictResult()
        result = predict_result.get_predict(request)
        return ResponseHelper().write(result)


class PredictHitrate(Resource):

    def get(self):
        set_access_log('PredictHitrate-get')

        predict_result = PredictResult()
        result = predict_result.get_hitrate_predict(request)
        return ResponseHelper().write(result)


class Scheduler(Resource):

    def get(self):
        set_access_log('Scheduler-get')

        predict_result = PredictResult()
        result = predict_result.get_schedule(request)

        return ResponseHelper().write(result)


class RealScore(Resource):

    def get(self):
        set_access_log('RealScore-get')

        predict_result = PredictResult()
        result = predict_result.get_real_score(request)

        return ResponseHelper().write(result)


class Train(Resource):

    def get(self):
        set_access_log('Train-get')

        predict_result = PredictResult()
        result = predict_result.get_train(request)
        return ResponseHelper().write(result)


api.add_resource(Predict, '/kbo_predict/predict')
api.add_resource(PredictHitrate, '/kbo_predict/predict_hitrate')
api.add_resource(Scheduler, '/kbo_predict/schedule')
api.add_resource(RealScore, '/kbo_predict/real_score')
api.add_resource(Train, '/kbo_predict/train')


class KboPitPoseTable(Resource):

    def get(self):
        set_access_log('KboPitPoseTable-get')

        pit_pose = PitPoseResult()
        result = pit_pose.get_pit_pose_data(request)

        return ResponseHelper().write(result)


api.add_resource(KboPitPoseTable, '/kbo_pit_pose')


class KboPitchTypeSchedule(Resource):

    def get(self):
        set_access_log('KboPitchTypeSchedule-get')

        pitch_type_result = PitchTypeResult()
        result = pitch_type_result.get_schedule(request)

        return ResponseHelper().write(result)


class KboPitchTypeGamePitList(Resource):

    def get(self):
        set_access_log('KboPitchTypeGamePitList-get')

        pitch_type_result = PitchTypeResult()
        result = pitch_type_result.get_game_ts_pit_by_gmkey(request)

        return ResponseHelper().write(result)


class KboPitchTypePitcherList(Resource):

    def get(self):
        set_access_log('KboPitchTypePitcherList-get')

        pitch_type_result = PitchTypeResult()
        result = pitch_type_result.get_game_ts_pitcher_by_gmkey(request)

        return ResponseHelper().write(result)


class KboPitchTypePitcherPitAllList(Resource):

    def get(self):
        set_access_log('KboPitchTypePitcherPitAllList-get')

        pitch_type_result = PitchTypeResult()
        result = pitch_type_result.get_game_ts_pit_by_pitcher_all(request)

        return ResponseHelper().write(result)


class KboPitchTypePredict(Resource):

    def get(self):
        set_access_log('KboPitchTypePredict-get')

        pitch_type_result = PitchTypeResult()
        result = pitch_type_result.get_predict(request)

        return ResponseHelper().write(result)


api.add_resource(KboPitchTypeSchedule, '/kbo_pitch_type/schedule')
api.add_resource(KboPitchTypeGamePitList, '/kbo_pitch_type/game_pit')
api.add_resource(KboPitchTypePitcherList, '/kbo_pitch_type/pitcher_list')
api.add_resource(KboPitchTypePitcherPitAllList, '/kbo_pitch_type/pitcher_pit')
api.add_resource(KboPitchTypePredict, '/kbo_pitch_type/predict')


if __name__ == '__main__':
    predict_g.initialize() # daehyuk test
    pitchtype_g.initialize()

    app.run(debug=True, host='0.0.0.0', port=21212)

if __name__ == 'api':
    try:
        print('Gunicorn Start')
        predict_g.initialize()
        pitchtype_g.initialize()
    except Exception as ex:
        print(ex)
