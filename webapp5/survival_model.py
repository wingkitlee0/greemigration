import numpy as np 
import joblib
import datetime
import pandas as pd

#from .basicmodel import BasicModel
from gcpredict.basicmodel import BasicModel

PRESENTDATE = datetime.date(2018, 1, 1) # make sure this is the same EVERYWHERE

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
    vec = [0.0] * (len(lst)-1)
    
    if x == lst[0]:
        return vec
    else:
        vec[d[x]-1] = 1.0
    return vec

class Util:
    """
    utility module to convert input values from web to the vector for sklearn.predict
    """
    def __init__(self):
        """
        constructor for Util
        """
        self.col_loc = {
            'CAT': 1,
            'CEN': 5,
            'COC': 10,
        }

    def convert_onehot(self, country, category, date1, center, app_type, concurrent):
        """
        Args:
            country:
            category:
            data1
            center
            app_type
            concurrent
        """
        vec = []

        # APP
        vec.append(app_type)
        # CAT: category
        vec.extend( convert2list(category, d['CAT_LIST']))
        # CEN: center
        vec.extend( convert2list(center, d['CEN_LIST']))
        # COC: country
        vec.extend( convert2list(country, d['COC_LIST']))
        # CON
        vec.append(concurrent)
        # START2, STARTM1, STARTM2

        start2 = (PRESENTDATE - date1).days
        startm1 = np.sin(date1.month/12.0 * 2.0 * np.pi)
        startm2 = np.cos(date1.month/12.0 * 2.0 * np.pi)

        vec.extend([start2, startm1, startm2])

        # STATUS, zero for input, but it is actually not used in Survival
        vec.append(0.0)

        print(len(vec))
        return vec
    
class SurvivalModel(BasicModel):
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
        BasicModel.__init__(self)
        self.modelfile = modelfile

        self.features = ['APP',
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

        self.util = Util()
        self.load_survival_model()

    def load_survival_model(self):
        self.cph = joblib.load(self.modelfile)    

    def predict(self, **params):

        input_vector = self.util.convert_onehot(**params)

        df = pd.DataFrame([input_vector], columns=self.features)

        sur = self.cph.predict_survival_function(df)

        times = sur[0].index.values
        sur_rate = sur[0].values

        idx1 = np.searchsorted(1-sur_rate, 0.25) # 75% survival
        idx2 = np.searchsorted(1-sur_rate, 0.5)  # median
        idx3 = np.searchsorted(1-sur_rate, 0.75) # 25% survival

        t25 = times[idx1]
        t50 = times[idx2]
        t75 = times[idx3]

        return times, sur_rate, t25, t50, t75




