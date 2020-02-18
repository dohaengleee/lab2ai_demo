from demo.kbo_pitch_type.db import GetDB
from demo.kbo_predict import globals as predict_g

DF_TEAM_NAME = None
DF_PERSON = None
DF_GAME_INFO_ALL = None
DF_CD_DETAIL = None


def initialize():
    try:
        global DF_TEAM_NAME
        global DF_PERSON
        global DF_GAME_INFO_ALL
        global DF_CD_DETAIL

        DF_TEAM_NAME = predict_g.DF_TEAM_NAME
        DF_PERSON = predict_g.DF_PERSON
        DF_GAME_INFO_ALL = predict_g.DF_GAME_INFO_ALL
        DF_CD_DETAIL = GetDB().stats_cd_detail()

    except Exception as e:
        print(e)


def get_player_name(gyear, pcode):
    if len(DF_PERSON[(DF_PERSON.gyear == gyear) & (DF_PERSON.pcode == str(pcode))]) > 0:
        return DF_PERSON[(DF_PERSON.gyear == gyear) & (DF_PERSON.pcode == str(pcode))].name.values[0]
    else:
        ''


def get_pit_kind_name(pit_kind_cd):
    if len(DF_CD_DETAIL[DF_CD_DETAIL.cd_se == pit_kind_cd]) > 0:
        return DF_CD_DETAIL[DF_CD_DETAIL.cd_se == pit_kind_cd].cd_nm.values[0]
    else:
        ''
