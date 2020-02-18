from demo.kbo_predict.lib.preprocessing import MakeDataSets
from demo.kbo_predict.db import GetDB
import config as c
import pandas as pd
import numpy as np
import pickle as pkl
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
import time


class Trainer:

    def __init__(self, years):
        self.years = years
        self.is_years = True if type(self.years) is list else False
        self.hitter = GetDB().hitter(years)
        self.pitcher = GetDB().pitcher(years)
        self.teamrank_daily = GetDB().teamrank_daily(years)
        self.entry = GetDB().entry(years)
        self.train_df = self.get_train_data()
        self.model = None
        self.training_time = None

    # def preprocessing(self):
    #     mds = MakeDataSets(str(year), self.pitcher, self.hitter, self.teamrank_daily)

    def get_train_data(self):
        train_df = pd.DataFrame()
        # 임시처리
        if self.is_years:
            for year in self.years:
                temp = MakeDataSets(str(year), self.pitcher, self.hitter,
                                    self.teamrank_daily, self.entry, is_training=True)
                temp.get_start_hitter_data()
                temp.get_hitter_data()
                temp.get_pitcher_data()
                temp.get_team_data()
                temp.drop_draw()
                temp.set_wls_to_dummy()
                temp.get_dummy_data()
                res = pd.concat([train_df, temp.result_df])
                train_df = res
        else:
            temp = MakeDataSets(str(self.years), self.pitcher, self.hitter,
                                self.teamrank_daily, self.entry, is_training=True)
            temp.get_start_hitter_data()
            temp.get_hitter_data()
            temp.get_pitcher_data()
            temp.get_team_data()
            temp.drop_draw()
            temp.set_wls_to_dummy()
            temp.get_dummy_data()
            train_df = temp.result_df

        train_df.fillna(int(0), inplace=True)
        try:
            train_df[c.cols['categorical_cols']] = train_df[c.cols['categorical_cols']].astype('category')
        except KeyError:
            c.cols['categorical_cols'].remove('Ateam_HD')
            c.cols['categorical_cols'].remove('Hteam_HD')
            train_df[c.cols['categorical_cols']] = train_df[c.cols['categorical_cols']].astype('category')
        train_df.reset_index(drop=True, inplace=True)

        return train_df

    def training(self):
        xgb_clf = xgb.XGBClassifier()
        xgb_param_grid = {
            "max_depth": np.arange(2, 4, 1),
            "subsample": np.arange(0.3, 0.6, 0.15),
            "learning_rate": np.arange(0.01, 0.11, 0.02),
            "min_child_weight": np.arange(1, 3, 1),
            "objective": ['binary:logistic'],
            "seed": [1024]
        }
        model = GridSearchCV(estimator=xgb_clf,
                             param_grid=xgb_param_grid,
                             scoring='roc_auc',
                             n_jobs=-1,
                             cv=2,
                             refit=True,
                             return_train_score=True)
        try:
            x = self.train_df[c.cols['train_cols']].values
            y = self.train_df.WLS.values
        except KeyError:
            c.cols['train_cols'].remove('Ateam_HD')
            c.cols['train_cols'].remove('Hteam_HD')
            x = self.train_df[c.cols['train_cols']].values
            y = self.train_df.WLS.values
        start = time.time()
        model.fit(x, y)
        end = time.time()
        self.training_time = end - start
        self.model = model

    def model_score(self):
        score_dict = {
            'best_params': self.model.best_params_,
            'best_score': str(self.model.best_score_),
            'training_time': str(self.training_time)
        }
        return score_dict

    def model_saver(self):
        if self.is_years:
            with open('demo/kbo_predict/model/model_{0}_to_{1}'.format(self.years[0], self.years[-1]), 'wb') as f:
                pkl.dump(self.model, f)
        else:
            with open('demo/kbo_predict/model/model_{0}'.format(self.years), 'wb') as f:
                pkl.dump(self.model, f)

