"""
This module deals with the preliminary data from the web UI to a dictionary for further conversion
"""
import datetime
from gcpredict.basicmodel import BasicModel

class ViewsUtil:
    def __init__(self):
        self.bm = BasicModel()
        pass

    def get_parameters_from_web_form(self, request):
        """
        convert the input from the web into a dictionary
        """

        myCountry = request.form['myCountry']
        category = request.form['myCategory']
        date1 = request.form['myDate']
        myCEN = request.form['myCenter']
        myAPP = request.form['myAppType']
        myCON = request.form['myCON']

        # convert to zero or 1
        myAPP = 1.0 if myAPP == 'Primary' else 0.0
        myCON = 1.0 if myCON == 'Concurrent' else 0.0
        if myCountry in self.bm.country_dict:
            myCountry = self.bm.country_dict[myCountry]
        else:
            myCountry = 'ROW'

        myCEN = self.bm.center_dict[myCEN] if myCEN in self.bm.center_dict else 'OTHER'

        print([myCountry, date1, myCEN, myAPP])
        if date1 == '':
            print("ERROR!! date is empty")
            date1 = datetime.date(2015, 1, 1)
        else:
            date1 = datetime.datetime.strptime(date1, '%m/%d/%Y').date()

        # this is the dictionary that stores the responses from the web form
        params = {
            'country': myCountry,
            'category': category,
            'date1': date1,
            'center': myCEN,
            'app_type': myAPP,
            'concurrent': myCON
        }

        return params
        