from flask import Flask
from flask import render_template, request

import datetime
import os

flask_app = Flask(__name__)

#@flask_app.route('/')
#def index():
#    return 'Hello Flask app'  

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    cpuCount = os.cpu_count()

    #mymodel = model.Model(modelfile=os.path.join(app.static_folder, MODELFILE))

    templateData = {
        'title' : 'Green Card Predictor',
        'time': timeString,
        'cpucount' : cpuCount,
        'country' : 'HK',
    #    'category_list' : mymodel.category_list,
    }
    if request.method == 'GET':
        return render_template('main.html', **templateData)
    #elif request.method == 'POST':
        #nationality = request.form['myCountry']
        #category = request.form['myCategory']
        #date1 = request.form['date1']
        #has_rfe = request.form['myRFE']

        #params = {
        #    'nationality' : nationality,
        #    'category' : category,
        #    'date1' : date1,
        #    'has_rfe' : has_rfe
        #}

        #prediction_date = mymodel.predict(**params)
        #print(request.args)
        #resultText = "You are from {} and applied the GC on {}.".format(nationality, date1)
        #results = {
        #    'text' : resultText,
        #    'prediction_date' : prediction_date,
        #}
        #return render_template('main.html', results=results, **templateData)