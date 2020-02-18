from demo.kbo_predict.db import GetDB
from demo.kbo_predict import util


DF_TEAM_NAME = None
DF_GAME_INFO_ALL = None
DF_PERSON = None


def initialize():
    try:
        global DF_TEAM_NAME
        global DF_GAME_INFO_ALL
        global DF_PERSON

        # DF_TEAM_NAME = GetDB().team_name()
        # DF_GAME_INFO_ALL = GetDB().gameinfo_all()
        # DF_PERSON = GetDB().person_all()

        # util.create_pickle_file('DF_TEAM_NAME', DF_TEAM_NAME)
        # util.create_pickle_file('DF_GAME_INFO_ALL', DF_GAME_INFO_ALL)
        # util.create_pickle_file('DF_PERSON', DF_PERSON)

        DF_TEAM_NAME = util.load_pickle_file('DF_TEAM_NAME')
        DF_GAME_INFO_ALL = util.load_pickle_file('DF_GAME_INFO_ALL')
        DF_PERSON = util.load_pickle_file('DF_PERSON')

    except Exception as e:
        print(e)
