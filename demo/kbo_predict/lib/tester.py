from demo.kbo_predict.db import GetDB
import config as c
from demo.kbo_predict import util as u
import pickle as pkl
import os
import pandas as pd
from demo.kbo_predict.lib.preprocessing import MakeDataSets


def load_model():
    # 임시
    # model_list = os.listdir('demo/kbo_predict/model/')
    with open('demo/kbo_predict/model/20200205_model_add_start_hitter_hra_v1', 'rb') as f:
        model = pkl.load(f)
    return model


def load_hitrate_model():
    with open('demo/kbo_predict/model/model_from_2017_to_2018.pickle', 'rb') as f:
        model = pkl.load(f)
    return model


def scheduler(year, month, hteam, ateam):
    return GetDB().gameinfo(year=year, month=month, hteam=hteam, ateam=ateam)


class Tester:

    def __init__(self, gmkey, predict_game=False):
        self.gmkey = gmkey
        self.years = 2019
        self.hitter = GetDB().hitter(self.years)
        if predict_game:
            self.model = load_model()
            self.pitcher = GetDB().pitcher(self.years)
            self.teamrank_daily = GetDB().teamrank_daily(self.years)
            self.season_2019_data = self.get_2019_data()
        else:
            self.hitrate_season_2019_data = pd.read_csv('demo/kbo_predict/data/hitrate_testset_2019.csv')
            self.hitrate_model = load_hitrate_model()

    def get_2019_data(self):
        # 임시
        data_list = os.listdir('demo/kbo_predict/data/')
        if data_list:
            #with open('demo/kbo_predict/data/'.format(data_list[-2]), 'rb') as f:
            with open('demo/kbo_predict/data/season_2019_add_start_hitters_hra_include_all_games', 'rb') as f:
                season_2019_data = pkl.load(f)
                return season_2019_data
        else:
            train_df = pd.DataFrame()
            temp = MakeDataSets(str(self.years), self.pitcher, self.hitter, self.teamrank_daily, is_training=False)
            temp.get_hitter_data()
            temp.get_pitcher_data()
            temp.get_team_data()
            temp.drop_draw()
            temp.set_wls_to_dummy()
            temp.get_dummy_data()
            res = pd.concat([train_df, temp.result_df])
            train_df = res

            train_df.fillna(int(0), inplace=True)
            try:
                train_df[c.cols['categorical_cols']] = train_df[c.cols['categorical_cols']].astype('category')
            except Exception:
                c.cols['categorical_cols'].remove('Ateam_HD')
                c.cols['categorical_cols'].remove('Hteam_HD')
                train_df[c.cols['categorical_cols']] = train_df[c.cols['categorical_cols']].astype('category')
            train_df.reset_index(drop=True, inplace=True)
            with open('./data/season_{}_data'.format(self.years), 'wb') as f:
                pkl.dump(train_df, f)

            return train_df

    def predict(self):
        target_game = self.season_2019_data[self.season_2019_data.gmkey == self.gmkey]
        try:
            x = target_game[c.cols['train_cols']].values
            predcit_result = self.model.predict_proba(x)
        except:
            c.cols['train_cols'].remove('Ateam_HD')
            c.cols['train_cols'].remove('Hteam_HD')
            x = target_game[c.cols['train_cols']].values
            predcit_result = self.model.predict_proba(x)

        return predcit_result

    def get_start_pitcher(self):
        result = {}
        n_df = self.pitcher[self.pitcher.gmkey == self.gmkey]
        era_df = self.season_2019_data[self.season_2019_data.gmkey == self.gmkey]
        if not (n_df.empty and era_df):
            result['a_pitcher'] = n_df[(n_df.start == "1") & (n_df.tb == 'T')].name.values[0]
            result['h_pitcher'] = n_df[(n_df.start == "1") & (n_df.tb == 'B')].name.values[0]
            result['a_pitcher_era'] = round(era_df.A_START_ERA_AVG.values[0], 2)
            result['h_pitcher_era'] = round(era_df.H_START_ERA_AVG.values[0], 2)

        return result



    def predict_hitrate(self):
        target_game = self.hitrate_season_2019_data[self.hitrate_season_2019_data.gmkey == self.gmkey]
        target_game = target_game.drop(columns=['gmkey', 'hitter', 'pitcher', 'catcher', 'hitter_turn'])
        target_game = target_game.astype({'hitter_code': 'int64', 'pitcher_code': 'int64', 'catcher_code': 'int64'})
        predcit_result = self.hitrate_model.predict_proba(target_game)
        result = pd.DataFrame(columns=['hitter', 'hitrate'])
        result['hitter'] = self.hitrate_season_2019_data[self.hitrate_season_2019_data.gmkey == self.gmkey]['hitter']
        result['hitrate'] = [i.max() for i in predcit_result]
        result['pcode'] = self.hitrate_season_2019_data[self.hitrate_season_2019_data.gmkey == self.gmkey]['hitter_code']
        result['turn'] = self.hitrate_season_2019_data[self.hitrate_season_2019_data.gmkey == self.gmkey]['hitter_turn']
        hitter_df = self.hitter[self.hitter.gmkey == self.gmkey]
        team_ls = []
        for pcd in result['pcode']:
            if hitter_df[hitter_df.pcode == str(pcd)].tb.values[0] == 'B':
                team_ls.append(hitter_df[hitter_df.pcode == str(pcd)].gmkey.values[0][10:12])
            else:
                team_ls.append(hitter_df[hitter_df.pcode == str(pcd)].gmkey.values[0][8:10])
        result['team'] = team_ls
        result = pd.merge(result[result.team == result.team.unique()[0]].sort_values('turn'),
                          result[result.team == result.team.unique()[1]].sort_values('turn'), how='outer')
        away = dict()
        away['team_code'] = ''
        away['team_name'] = ''
        away['hitter_list'] = []
        home = dict()
        home['team_code'] = ''
        home['team_name'] = ''
        home['hitter_list'] = []
        for i, row in result.iterrows():
            if len(away['team_code']) == 0:
                away['team_code'] = row['team']
                away['team_name'] = u.get_team_name(row['team'])
            if away['team_code'] == row['team']:
                away['hitter_list'].append(dict(row.drop('team')))
            else:
                if len(home['team_code']) == 0:
                    home['team_code'] = row['team']
                    home['team_name'] = u.get_team_name(row['team'])
                home['hitter_list'].append(dict(row.drop('team')))
        res = [away, home]

        return res

    def real_score(self):
        df = GetDB().score(self.gmkey)
        score = df[df.gmkey == self.gmkey].to_dict('records')
        score = {k: v for k, v in score[0].items() if v != -1}

        return score
