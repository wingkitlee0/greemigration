import numpy as np 
import joblib
import datetime

import sklearn


from . import modelutil as mu
from .basicmodel import BasicModel

class Model(BasicModel):
    def __init__(self, modelfile):
        BasicModel.__init__(self)
        self.modelfile = modelfile

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

