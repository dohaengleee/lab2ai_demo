from demo.kbo_predict import globals as g
import pickle


def get_team_name(team_code):
    if len(g.DF_TEAM_NAME[g.DF_TEAM_NAME.team == team_code].team_kor.values) > 0:
        return g.DF_TEAM_NAME[g.DF_TEAM_NAME.team == team_code].team_kor.values[0]
    else:
        return ''


def get_person_back_no(year, pcode):
    if len(g.DF_PERSON[(g.DF_PERSON.gyear == int(year)) & (g.DF_PERSON.pcode == pcode)].backnum.values) > 0:
        return g.DF_PERSON[(g.DF_PERSON.gyear == int(year)) & (g.DF_PERSON.pcode == pcode)].backnum.values[0]
    else:
        return ''

def create_pickle_file(file_name, data):
    with open('demo/kbo_predict/pickle_data/{}.pickle'.format(file_name), 'wb') as f:
        pickle.dump(data, f)


def load_pickle_file(file_name):
    with open('demo/kbo_predict/pickle_data/{}.pickle'.format(file_name), 'rb') as f:
        return pickle.load(f)
