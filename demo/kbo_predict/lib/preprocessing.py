import pandas as pd


class MakeDataSets(object):

    def __init__(self, year, pitcher, hitter, teamrank_daily, entry, is_training=False):
        self.year = year
        self.training = is_training
        self.pitcher = pitcher
        self.hitter = hitter
        self.teamrank_daily = teamrank_daily
        self.entry = entry
        self.result_df = pd.DataFrame()
        self.set_dsets_by_year()
        self.get_team_date()
        self.total_pitcher = self.get_pitcher_total()
        self.total_hitter = self.get_hitter_total()

    def set_dsets_by_year(self):
        self.pitcher = self.pitcher[self.pitcher.gmkey.str.startswith(self.year)].reset_index(drop=True)
        self.hitter = self.hitter[self.hitter.gmkey.str.startswith(self.year)].reset_index(drop=True)
        self.entry = self.entry[self.entry.gmkey.str.startswith(self.year)].reset_index(drop=True)
        self.teamrank_daily = self.teamrank_daily[self.teamrank_daily.gyear == self.year].reset_index(drop=True)
        self.teamrank_daily = self.teamrank_daily[self.teamrank_daily.date.ge(self.pitcher.loc[0].gday)].reset_index(
            drop=True)

    def get_team_date(self):
        self.result_df['gmkey'] = self.pitcher.gmkey
        self.result_df['date'] = [i[:8] for i in self.pitcher.gmkey.tolist()]
        self.result_df['Hteam'] = [i[10:12] for i in self.pitcher.gmkey.tolist()]
        self.result_df['Ateam'] = [i[8:10] for i in self.pitcher.gmkey.tolist()]
        self.result_df.drop_duplicates(keep='first', inplace=True)
        self.result_df.reset_index(drop=True, inplace=True)

    def get_hitter_total(self):
        temp = []
        for i in range(len(self.hitter[self.hitter.name == '합계'])):
            if self.hitter[self.hitter.name == '합계'].iloc[i].tb == 'B':
                temp.append(self.hitter[self.hitter.name == '합계'].iloc[i].gmkey[10:12])
            else:
                temp.append(self.hitter[self.hitter.name == '합계'].iloc[i].gmkey[8:10])
        df = self.hitter[self.hitter.name == '합계']
        df['team'] = temp
        df.reset_index(drop=True, inplace=True)
        return df

    def get_pitcher_total(self):
        temp = []
        for i in range(len(self.pitcher[self.pitcher.name == '합계'])):
            if self.pitcher[self.pitcher.name == '합계'].iloc[i].tb == 'B':
                temp.append(self.pitcher[self.pitcher.name == '합계'].iloc[i].gmkey[10:12])
            else:
                temp.append(self.pitcher[self.pitcher.name == '합계'].iloc[i].gmkey[8:10])
        df = self.pitcher[self.pitcher.name == '합계']
        df['team'] = temp
        df.reset_index(drop=True, inplace=True)
        return df

    # region cal_method
    @staticmethod
    def cal_run_avg(hitter_df, team, date):
        temp_df = hitter_df[hitter_df.team == team]
        result_df = temp_df[temp_df.gday.lt(date)]
        RUN_AVG = round(result_df.run.sum() / len(result_df), 2)
        return RUN_AVG

    @staticmethod
    def cal_hra_avg(hitter_df, team, date):
        temp_df = hitter_df[hitter_df.team == team]
        result_df = temp_df[temp_df.gday.lt(date)]
        HRA_AVG = round(result_df.hit.sum() / result_df.ab.sum(), 3)
        return HRA_AVG

    @staticmethod
    def cal_start_era_avg(pitcher_df, gmkey, date, tb):
        temp_df = pitcher_df[pitcher_df.gmkey == gmkey]
        name = temp_df[(temp_df.start == '1') & (temp_df.tb == tb)].name.values[0]
        result_df = pitcher_df.loc[(pitcher_df.gday.lt(date)) & (pitcher_df.name == name)]
        ERA_AVG = round((result_df.er.sum() / sum((result_df.inn2 / 3))) * 9, 2)
        return ERA_AVG

    @staticmethod
    def cal_start_hra_avg(hitter_df, pcode, date):
        temp_df = hitter_df[hitter_df.pcode == str(pcode)]
        result_df = temp_df[temp_df.gday.lt(date)]
        HRA_AVG = round(result_df.hit.sum() / result_df.ab.sum(), 3)
        return HRA_AVG

    @staticmethod
    def cal_r_avg(pitcher_df, team, date):
        temp_df = pitcher_df[pitcher_df.team == team]
        result_df = temp_df[temp_df.gday.lt(date)]
        R_AVG = round(result_df.r.sum() / len(result_df), 2)
        return R_AVG

    @staticmethod
    def cal_era_avg(pitcher_df, team, date):
        temp_df = pitcher_df[pitcher_df.team == team]
        result_df = temp_df[temp_df.gday.lt(date)]
        ERA_AVG = round((result_df.er.sum() / sum((result_df.inn2 / 3))) * 9, 2)
        return ERA_AVG

    @staticmethod
    def get_wra(rank_df, team, date):
        try:
            temp_df = rank_df[rank_df.team == team]
            result_df = temp_df[temp_df.date.lt(date)]
            return result_df.iloc[-1].wra
        except:
            return 0

    # endregion cal_method

    def get_hitter_data(self):
        run_avg_home = []
        run_avg_away = []

        for i in range(len(self.result_df)):
            result_home = self.cal_run_avg(self.total_hitter, self.result_df.iloc[i].Hteam, self.result_df.iloc[i].date)
            result_away = self.cal_run_avg(self.total_hitter, self.result_df.iloc[i].Ateam, self.result_df.iloc[i].date)
            run_avg_home.append(result_home)
            run_avg_away.append(result_away)

        hra_home = []
        hra_away = []
        for i in range(len(self.result_df)):
            result_home = self.cal_hra_avg(self.total_hitter, self.result_df.iloc[i].Hteam, self.result_df.iloc[i].date)
            result_away = self.cal_hra_avg(self.total_hitter, self.result_df.iloc[i].Ateam, self.result_df.iloc[i].date)
            hra_home.append(result_home)
            hra_away.append(result_away)

        self.result_df['H_RUN_AVG'] = run_avg_home
        self.result_df['A_RUN_AVG'] = run_avg_away
        self.result_df['H_HRA_AVG'] = hra_home
        self.result_df['A_HRA_AVG'] = hra_away

    def get_start_hitter_data(self):
        cols = ['gmkey']
        for i in range(10):
            if i == 0:
                continue
            cols.append('hitter_h_{}'.format(i))
            cols.append('hitter_a_{}'.format(i))
        start_hitters_df = pd.DataFrame(columns=cols)
        start_hitters_df['gmkey'] = self.result_df.gmkey
        for idx, gmkey in enumerate(start_hitters_df.gmkey):
            start_hitters = self.entry[self.entry.gmkey == gmkey][
                self.entry[self.entry.gmkey == gmkey].turn.str.startswith('1')]
            start_hitters = start_hitters[~start_hitters.turn.str.contains('0')]
            for tb, df in start_hitters.groupby('team', sort='turn'):
                df.drop_duplicates(['name'], keep='first', inplace=True)
                for c, pcd in enumerate(df.pcode):
                    if tb == 'B':
                        start_hitters_df.loc[idx].at['hitter_h_{}'.format(c+1)] = self.cal_start_hra_avg(self.hitter,
                                                                                                         pcd,
                                                                                                         gmkey)
                    else:
                        start_hitters_df.loc[idx].at['hitter_a_{}'.format(c + 1)] = self.cal_start_hra_avg(self.hitter,
                                                                                                           pcd,
                                                                                                           gmkey)
        self.result_df = pd.merge(self.result_df, start_hitters_df)

    def get_pitcher_data(self):
        r_avg_home = []
        r_avg_away = []
        for i in range(len(self.result_df)):
            result_home = self.cal_r_avg(self.total_pitcher, self.result_df.iloc[i].Hteam, self.result_df.iloc[i].date)
            result_away = self.cal_r_avg(self.total_pitcher, self.result_df.iloc[i].Ateam, self.result_df.iloc[i].date)
            r_avg_home.append(result_home)
            r_avg_away.append(result_away)

        era_avg_home = []
        era_avg_away = []
        for i in range(len(self.result_df)):
            result_home = self.cal_era_avg(self.total_pitcher, self.result_df.iloc[i].Hteam,
                                           self.result_df.iloc[i].date)
            result_away = self.cal_era_avg(self.total_pitcher, self.result_df.iloc[i].Ateam,
                                           self.result_df.iloc[i].date)
            era_avg_home.append(result_home)
            era_avg_away.append(result_away)

        start_era_avg_home = []
        start_era_avg_away = []
        for i in range(len(self.result_df)):
            result_home = self.cal_start_era_avg(self.pitcher, self.result_df.iloc[i].gmkey,
                                                 self.result_df.iloc[i].date, 'B')
            result_away = self.cal_start_era_avg(self.pitcher, self.result_df.iloc[i].gmkey,
                                                 self.result_df.iloc[i].date, 'T')
            start_era_avg_home.append(result_home)
            start_era_avg_away.append(result_away)

        self.result_df['H_R_AVG'] = r_avg_home
        self.result_df['A_R_AVG'] = r_avg_away
        self.result_df['H_ERA_AVG'] = era_avg_home
        self.result_df['A_ERA_AVG'] = era_avg_away
        self.result_df['H_START_ERA_AVG'] = start_era_avg_home
        self.result_df['A_START_ERA_AVG'] = start_era_avg_away

    def get_team_data(self):
        self.teamrank_daily.replace({'KT': 'KT', 'LG': 'LG', 'NC': 'NC', 'SK': 'SK', '기아': 'HT',
                                     '두산': 'OB', '롯데': 'LT', '삼성': 'SS', '우리': 'WO', '한화': 'HH'}, inplace=True)
        wra_avg_home = []
        wra_avg_away = []
        for i in range(len(self.result_df)):
            result_home = self.get_wra(self.teamrank_daily, self.result_df.iloc[i].Hteam, self.result_df.iloc[i].date)
            result_away = self.get_wra(self.teamrank_daily, self.result_df.iloc[i].Ateam, self.result_df.iloc[i].date)
            wra_avg_home.append(result_home)
            wra_avg_away.append(result_away)

        self.result_df['H_WRA_AVG'] = wra_avg_home
        self.result_df['A_WRA_AVG'] = wra_avg_away

    def drop_draw(self):
        if self.training:
            drop_idx = []
            for i in self.total_pitcher[self.total_pitcher.wls == 'D'].gmkey:
                drop_idx.append(self.result_df[self.result_df.gmkey == i].index.values[0])
            self.result_df.drop(index=drop_idx, inplace=True)
            self.result_df.reset_index(drop=True, inplace=True)

    def set_wls_to_dummy(self):
        if self.training is not True:
            self.result_df['WLS'] = self.total_pitcher[
                (self.total_pitcher.wls == 'W') | (self.total_pitcher.wls == 'D')]\
                .drop_duplicates(subset='GMKEY', keep='first').tb.tolist()
            self.result_df.replace({'WLS': {'B': 1, 'T': 0}}, inplace=True)
        else:
            self.result_df['WLS'] = self.total_pitcher[self.total_pitcher.wls == 'W'].tb.tolist()
            self.result_df.replace({'WLS': {'B': 1, 'T': 0}}, inplace=True)

    def get_dummy_data(self):
        self.result_df = pd.get_dummies(self.result_df, columns=['Hteam', 'Ateam'])
        self.result_df.WLS.astype('category')



