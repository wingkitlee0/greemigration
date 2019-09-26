import numpy as np 
import joblib
import datetime
import sklearn

from model import BasicModel

"""
['APP',
 'CAT_EB2',
 'CAT_EB2-NIW',
 'CAT_EB3',
 'CAT_OTHER',
 'CEN_NBC',
 'CEN_NE',
 'CEN_OTHER',
 'CEN_TX',
 'CEN_VT',
 'COC_India',
 'COC_Mexico',
 'COC_ROW',
 'CON',
 'START2',
 'STARTM1',
 'STARTM2',
 'STATUS']
"""

d = {
    'CAT_LIST' : ['EB1', 'EB2', 'EB2-NIW', 'EB3', 'OTHER'],
    'CEN_LIST' : ['CA', 'NBC', 'NE', 'OTHER', 'TX', 'VT'],
    'COC_LIST' : ['China', 'India', 'Mexico', 'ROW'],
}

def convert2list(x, lst, default_last=True):
    d = {k: i for i, k in enumerate(lst)}
    vec = [0] * (len(lst)-1)
    
    if x == lst[0]:
        return vec
    else:
        vec[d[x]-1] = 1
    return vec

class Util:
    def __init__(self):
        self.col_loc = {
            'CAT': 1,
            'CEN': 5,
            'COC': 10,
        }

    def convert_onehot(country, category, data1, center, app_type, concurrent):
        vec = []

        # APP
        vec.append( 1 if app_type == 'Primary' else 0)
        # CAT: category
        vec.append( convert2list(category, d['CAT_LIST'])
        # CEN: center
        vec.append( convert2list(center, d['CEN_LIST']))
        # COC: country
        vec.append( convert2list(country, d['COC_LIST']))
        # CON
        vec.append( 1 if concurrent == 'Concurrent' else 0)
        # START2
        

        return vec
    



class SurvivalModel(Model):
    """
            params = {
            'myCountry': myCountry,
            'category': category,
            'date1': date1,
            'myCEN': myCEN,
            'myAPP': myAPP,
            'myCON': myCON
        }
    """
    def __init__(self, modelfile):
        self.modelfile = modelfile

        self.load_clf()

    def load_clf(self):
        self.clf = joblib.load(self.modelfile)    

    def predict(self, **params):
        myCountry = params['myCountry']
        myCAT = params['category']
        myCEN = params['myCEN']
        myAPP = 

        if params['date1'] == '':
            return 0

        start_date = datetime.datetime.strptime(params['date1'], '%m/%d/%Y').date()
        # has_rfe = params['has_rfe'] == 'Yes'


        input_vector = [self.mymodelutil.convert_onehot(myCountry, category, start_date)]

        return int(self.clf.predict(input_vector)[0])