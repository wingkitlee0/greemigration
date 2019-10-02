from flask import render_template, abort, Response, request

# from bokeh.plotting import figure
# from bokeh.embed import components
# from bokeh.models import Range1d
from .bokehplot import BokehPlot

import pandas as pd

import datetime
import os

from . import app, model, survival_model
from gcpredict.basicmodel import BasicModel

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

    templateData = {
        'title': 'Greemigration',
        'tagline': 'surviving the waiting of green card',
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

        # PREDICTIONS FROM MODEL
        inp = mymodel.convert_onehot(**params)
        sm = survival_model.SurvivalModel(os.path.join(app.static_folder, MODELFILE))
        sm.load_survival_model()
        times, sur_rate, t25, t50, t75 = sm.predict(**params)
        prediction_days = t50
        print("25%, 50%, 75% = {} {} {}".format(t25, t50, t75))
        
        # # PLOT WITH BOKEH
        # plot = figure(plot_width=500, plot_height=300, 
        #     x_axis_label='Waiting Time [days]',
        #     y_axis_label='Approval Ratio')
        # plot.xaxis.axis_label_text_font_size = "20pt"
        # plot.yaxis.axis_label_text_font_size = "20pt"
        # plot.xaxis.axis_label_text_font_style = "normal"
        # plot.yaxis.axis_label_text_font_style = "normal"

        # # vertical line below the median dot
        # plot.line([t50, t50], [-100, 0.5], line_width=3, line_dash='dashed', line_color='black')
        # # main curve
        # plot.line(times, 1.0-sur_rate, line_width=5)
        # # median dot
        # plot.circle(t50, 0.5, legend="median", fill_color="white", size=12)
        
        # plot.x_range=Range1d(0, 2000)
        # plot.y_range=Range1d(0, 1.05)
        # plot.legend.location = "bottom_right"
        # from bokeh.models import NumeralTickFormatter
        # plot.yaxis.formatter = NumeralTickFormatter(format='0 %')
        # plot_script, plot_div = components(plot)
        myplot = BokehPlot()
        plot_script, plot_div = myplot.make_bokeh_plot(times, sur_rate, t50)

        templateData['plot_script'] = plot_script
        templateData['plot_div'] = plot_div

        
        resultText = "You have submitted the green card application on {}.".format(myCountry, date1)
        results = {
            'text' : resultText,
            'prediction_date' : "{:4.1f}".format(prediction_days / 30.0),
            't75': "{:4.1f}".format(t75 / 30.0),
            'input' : inp,
        }
        return render_template('main.html', results=results, **templateData)
