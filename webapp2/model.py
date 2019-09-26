import numpy as np 
import joblib
import datetime

import sklearn


from . import modelutil as mu

class Model:
    def __init__(self, modelfile):
        self.modelfile = modelfile

        self.category_list = [
            'EB1',
            'EB2',
            'EB2-NIW',
            'EB3',
        ]

        self.center_dict = {
             'National Benefit Center': 'NBC',
             'California': 'CA',
             'Nebraska': 'NE',
             'Texas': 'TX',
             'Vermont': 'VT',
             'OTHER': 'OTHER'
        }
        self.center_list = [k for k in self.center_dict]

        self.columns = ['RFE', 'START2', 'COUNTRY2_India', 'COUNTRY2_Mexico', 'COUNTRY2_ROW',
            'CAT_EB2', 'CAT_EB2-NIW', 'CAT_EB3']

        self.mymodelutil = mu.ModelUtil(columns=self.columns)

        self.load_clf()

    def load_clf(self):
        self.clf = joblib.load(self.modelfile)    

    def predict(self, **params):
        myCountry = params['myCountry']
        category = params['category']

        if params['date1'] == '':
            return 0

        start_date = datetime.datetime.strptime(params['date1'], '%m/%d/%Y').date()
        # has_rfe = params['has_rfe'] == 'Yes'


        input_vector = [self.mymodelutil.convert_onehot(myCountry, category, start_date)]

        return int(self.clf.predict(input_vector)[0])

