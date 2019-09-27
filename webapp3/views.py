from flask import render_template, abort, Response, request

from bokeh.plotting import figure
from bokeh.embed import components

import pandas as pd

import datetime
import os

from . import app, model, survival_model
from .basicmodel import BasicModel

#MODELFILE = 'data/clf.joblib'
MODELFILE = 'data/cph_sep26_3.cpk'

@app.route('/', methods=['GET', 'POST'])
def main():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    cpuCount = os.cpu_count()

    #mymodel = model.Model(modelfile=os.path.join(app.static_folder, MODELFILE))
    mymodel = survival_model.Util()
    bm = BasicModel()
    
    plot_script = ""
    plot_div = ""

    templateData = {
        'title': 'Greemigration',
        'tagline': 'surviving the long line',
        'project_description': 'This web app provides waiting predictions for employment-based applications',
        'time': timeString,
        'cpucount' : cpuCount,
        'country' : 'HK',
        'category_list' : bm.category_list,
        'center_list' : bm.center_list,
        'plot_script': plot_script, 
        'plot_div': plot_div,
    }
    if request.method == 'GET':
        return render_template('main.html', **templateData)
    elif request.method == 'POST':
        myCountry = request.form['myCountry']
        category = request.form['myCategory']
        date1 = request.form['date1']
        myCEN = request.form['myCenter']
        myAPP = request.form['myAppType']
        myCON = request.form['myCON']

        # convert to zero or 1
        myAPP = 1.0 if myAPP == 'Primary' else 0.0
        myCON = 1.0 if myCON == 'Concurrent' else 0.0
        if myCountry in bm.country_dict:
            myCountry = bm.country_dict[myCountry]
        else:
            myCountry = 'ROW'

        myCEN = bm.center_dict[myCEN] if myCEN in bm.center_dict else 'OTHER'

        print([myCountry, date1, myCEN, myAPP])
        if date1 == '':
            print("ERROR!! date is empty")
            date1 = datetime.date(2015, 1, 1)
        else:
            date1 = datetime.datetime.strptime(date1, '%m/%d/%Y').date()

        params = {
            'country': myCountry,
            'category': category,
            'date1': date1,
            'center': myCEN,
            'app_type': myAPP,
            'concurrent': myCON
        }

        #prediction_date = mymodel.predict(**params)
        inp = mymodel.convert_onehot(**params)

        sm = survival_model.SurvivalModel(os.path.join(app.static_folder, MODELFILE))
        sm.load_survival_model()
        #df = sm.predict(**params)
        #sur = sm.cph.predict_survival_function(df)
        #prediction_date = sm.cph.predict_median(df)

        #xx = sur[0].index.values
        #yy = sur[0].values
        
        times, sur_rate, t25, t50, t75 = sm.predict(**params)
        prediction_date = t50

        print("25%, 50%, 75% = {} {} {}".format(t25, t50, t75))
        
        plot = figure(plot_width=500, plot_height=300, 
            x_axis_label='Waiting Time [days]',
            y_axis_label='Cumulated Approval Fraction')
        plot.line(times, 1.0-sur_rate, line_width=5)
        plot.circle(t50, 0.5, legend="median", fill_color="white", size=12)
        plot_script, plot_div = components(plot)
        templateData['plot_script'] = plot_script
        templateData['plot_div'] = plot_div

        
        resultText = "You have submitted the green card application on {}.".format(myCountry, date1)
        results = {
            'text' : resultText,
            'prediction_date' : prediction_date,
            'input' : inp,
        }
        return render_template('main.html', results=results, **templateData)
