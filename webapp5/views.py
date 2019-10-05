import pandas as pd
import datetime
import os
from flask import render_template, abort, Response, request

from . import app, model, survival_model
from gcpredict.basicmodel import BasicModel

from .views_util import ViewsUtil
from .bokehplot import BokehPlot

MODELFILE = 'data/cph_sep26_3.cpk'

@app.route('/', methods=['GET', 'POST'])
def main():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    cpuCount = os.cpu_count()

    mymodel = survival_model.Util()
    bm = BasicModel()
    
    plot_script = ""
    plot_div = ""

    # default values
    templateData = {
        'title': 'Greemigration',
        'tagline': 'surviving the waiting of green card',
        'project_description': 'This web app provides waiting predictions for employment-based applications',
        'time': timeString,
        'cpucount' : cpuCount,
        'country' : 'HK',
        'center' : 'Texas',
        'category' : 'EB1',
        'category_list' : bm.category_list,
        'center_list' : bm.center_list,
        'apptype': 'Primary',
        'concurrency': 'Concurrent',
        'plot_script': plot_script, 
        'plot_div': plot_div,
    }
    if request.method == 'GET':
        return render_template('main.html', **templateData)
    elif request.method == 'POST':
        # get params
        myview = ViewsUtil()
        params = myview.get_parameters_from_web_form(request)

        # PREDICTIONS FROM MODEL
        inp = mymodel.convert_onehot(**params)
        sm = survival_model.SurvivalModel(os.path.join(app.static_folder, MODELFILE))
        sm.load_survival_model()
        times, sur_rate, t25, t50, t75 = sm.predict(**params)
        prediction_days = t50
        print("25%, 50%, 75% = {} {} {}".format(t25, t50, t75))
        
        myplot = BokehPlot()
        plot_script, plot_div = myplot.make_bokeh_plot(times, sur_rate, t50)
        # update the template data and re-populate the data from the web form
        templateData['country'] = request.form['myCountry']
        templateData['center'] = request.form['myCenter']
        templateData['category'] = request.form['myCategory']
        templateData['apptype'] = request.form['myAppType']
        templateData['concurrency'] = request.form['myCON']

        templateData['plot_script'] = plot_script
        templateData['plot_div'] = plot_div

        # the result text is shown only after pressing the Predict! buttion
        resultText = "You have submitted the green card application on {}.".format(params['country'], params['date1'])
        results = {
            'text' : resultText,
            'prediction_date' : "{:4.1f}".format(prediction_days / 30.0),
            't75': "{:4.1f}".format(t75 / 30.0),
            'input' : inp,
        }

        return render_template('main.html', results=results, **templateData)
