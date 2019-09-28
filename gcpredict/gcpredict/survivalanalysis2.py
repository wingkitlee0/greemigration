import numpy as np
import pandas as pd
import datetime
from collections import Counter

PRESENTDATE_DEFAULT = datetime.date(2018, 1, 1)

def convert_str_date(s):
    try:
        return datetime.datetime.strptime(s.strip(' '), '%m/%d/%Y')
    except ValueError:
        return np.NaN

class Survival:
    def __init__(self, df, 
            presentdate=PRESENTDATE_DEFAULT,
            include_future=False,
            set_future_pending=True,
            ):
        self.presentdate = presentdate
        self.include_future = include_future
        self.set_future_pending = set_future_pending

        if not self.include_future:
            self.df = df[df['START'] < self.presentdate]
        else:
            self.df = df

        # create a one-hot column for approval
        if 'STATUS' not in self.df.columns:
            self.df.loc[:, 'STATUS'] = self.df.loc[:, 'I-485 Status'].apply(lambda x: 1 if x == ' approved' else 0)

        # header / columns
        self.header = self.df.columns
        self.header_r = { v:k+1 for k, v in enumerate(self.header)} # +1 because 0th-index refers to 'index'
        
        # service center
        # remove cases without service center
        self.df = self.df[self.df['Service Center'] != ' ']

        counter_center = Counter(self.df['Service Center'])
        CEN_list = [k for k in counter_center]
        CEN_abr_list = ['CA', 'TX', 'NE', 'VT', 'NBC', 'CHI', 'DA', 'PH', 'PO', 'NA']
        self.CEN_dict = { k: v for k, v in zip(CEN_list, CEN_abr_list)}

        self.setup()

        if self.set_future_pending:
            self.set_future_approved_cases_as_pending()
        
    def setup(self):
        """
        put all the operations here
        """
        # add month as a feature
        self.df.loc[:, 'STARTM'] = self.df.loc[:, 'START'].apply(lambda x: x.month)
            
        # remove approved cases without dates
        self.df = self.df[~ ((self.df['I-485 Approval/Denial Date'] == ' ') & (self.df['STATUS'] == 1))]

        # assign DT: end-start for approved case, present-start for pending cases
        self.df.loc[:, 'DT'] = [self.get_dt(row) for row in self.df.itertuples() ]

        # add end date
        # pending cases with have NaT
        self.df.loc[:, 'END'] = self.df.loc[:, 'I-485 Approval/Denial Date'].apply(convert_str_date)


        # add a column for service centers
        def get_cen(x):
            cen = self.CEN_dict[x]
            if cen in ['CHI', 'DA', 'PH', 'PO', 'NA']:
                return 'OTHER'
            else:
                return cen
        self.df.loc[:,'CEN'] = self.df.loc[:, 'Service Center'].apply(lambda x: get_cen(x))

        # applicant type -> 1 or 0
        # replace ' ' to primary
        self.df.loc[:, 'APP'] = self.df.loc[:, 'Applicant Type'].apply(lambda x: 1 if x in [' primary', ' '] else 0)

        # received RFE or not
        # assuming no entry means no RFE
        # they could be pending too, so it's a little bit optimistic here
        self.df.loc[:, 'RFE'] = self.df.loc[:, 'RFE Received?'].apply(lambda x: 0 if [' ', ' no'] else 1)

        # year
        self.df.loc[:, 'YEAR'] = self.df.loc[:, 'START'].apply(lambda x: x.year)

        # conconcurrent
        self.df.loc[:, 'CON'] = self.df.loc[:, 'I-140/I-485 Filing'].apply(lambda x: 1 if x == ' concurrent' else 0)

    def get_dt(self, row):
        hdr = self.header_r
        if row[hdr['STATUS']] == 0:
            return row[hdr['START2']]
        else:
            # approved case
            end = convert_str_date(row[hdr['I-485 Approval/Denial Date']]).date()
            start = row[hdr['START']]
            return (end-start).days

    def set_future_approved_cases_as_pending(self):
        """
        set future approved cases as pending:

        "Future" means submission date is after present day default 
        """

        FUTURE_APPROVED = ( (pd.isnull(self.df['END'])) | (self.df['END'] > pd.Timestamp(self.presentdate)) )

        APPROVED = (self.df['I-485 Status'] == ' approved')

        idx = self.df[FUTURE_APPROVED & APPROVED].index.values # index array
        
        # set the status to pending
        self.df.loc[idx, 'STATUS'] = 0

        #
        self.df.loc[idx, 'DT'] = self.df.loc[idx, 'START2']


    def get_simple_mean_model(self, X, y):
        """
        return a set of wait-time predictions simply based on the country's mean
        """

        y_ = y.copy()
        y_.loc[:] = 0

        country_list = ['ROW', 'India', 'China', 'Mexico']

        def country_selector(X, c):
            if c in ['ROW', 'India', 'Mexico']:
                return (X['COC_{}'.format(c)] == 1) & (X['STATUS']==1)
            else:
                return (X['COC_India'] == 0) & (X['COC_ROW'] == 0) & (X['STATUS']==1)

        self.country_mean = { c:y[country_selector(X, c)].mean() for c in country_list}

        for i in X.index:
            cty = [X.at[i, 'COC_{}'.format(c)] for c in ['ROW', 'India', 'Mexico']]
            if cty == [0, 0, 0]: # China
                y_.loc[i] = self.country_mean['China']
            if cty == [1, 0, 0]: # ROW
                y_.loc[i] = self.country_mean['ROW']
            if cty == [0, 1, 0]: # India
                y_.loc[i] = self.country_mean['India']
            if cty == [0, 0, 1]: # Mexico
                y_.loc[i] = self.country_mean['Mexico']
            #y_.loc[i] = np.min(y_.loc[i], X.loc[i, 'START2'])

        y_ = pd.Series([min(y_.loc[i], X.loc[i, 'START2']) for i in y_.index], name='DT', index=y.index)
        return y_