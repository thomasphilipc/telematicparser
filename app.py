from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response, send_file
from flask_wtf import FlaskForm
from wtforms import StringField,FileField,TextAreaField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField
from werkzeug import secure_filename
import os

import datetime
import json
import babel
import teltonikaparser
import distacalc


app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class TeltonikaForm(FlaskForm):
    data = StringField('Raw Data', validators=[DataRequired()])


class CargoForm(FlaskForm):
    data = TextAreaField('KML')
    distance_threshold = TextAreaField('Threshold',validators=[DataRequired()])
    filter_threshold = TextAreaField('Filter Threshold',validators=[DataRequired()])
    file = FileField()

@app.route('/')
def home():
    return  ('Home')

@app.route('/teltonika/',methods=['GET', 'POST'])
def parseteltonika():
    form = TeltonikaForm()
    parsed=""
    if request.method == 'POST' and form.validate_on_submit():
        flash('Form valid')
        if request.form['data']:
            rawdata=request.form['data']
            #debug purpose

            print("rawdata {}".format(rawdata))
            parsed=teltonikaparser.parsed_data(rawdata)
            print("parsed data : {}".format(parsed))
            #prepare json
            data = {}
            data['parsed'] = parsed
            json_data = json.dumps(data)
            result = json.loads(json_data)
            return render_template('teltonika/teltonikaparsed.html',
                            result = result)
        else:
            flash('All the form fields are required. ')
            return render_template('teltonika/teltonika.html',form=form)

    else:

        return render_template('teltonika/teltonika.html',form=form)

@app.route('/cargo/',methods=['GET', 'POST'])
def cargo():
    form = CargoForm()


    if request.method == 'POST' and form.validate_on_submit():
        flash('Form Valid')
        if request.form['distance_threshold']:

            distance_threshold = request.form['distance_threshold']
            filter_threshold = request.form['filter_threshold']


            #call function to process the data
            filename = secure_filename(form.file.data.filename)
            print(filename)
            form.file.data.save('uploads/' +filename)
            base=os.path.basename(filename)
            filenamewithoutextention = os.path.splitext(base)
            reduction=distacalc.sanitizeroute(filename,distance_threshold,filter_threshold)

            data = {}
            data['filelocation'] = filenamewithoutextention[0]
            data['distance_threshold'] = distance_threshold
            data['filter_threshold'] = filter_threshold
            data['reduction']=reduction
            json_data = json.dumps(data)
            result = json.loads(json_data)
            iframe = filenamewithoutextention[0]+".html"
            return render_template('cargo/cargoresult.html',result=result, iframe=iframe)
    else:
        return render_template('cargo/cargo.html',form=form)

@app.route('/cargo/get_map/<filename>')
def get_map(filename):

    return send_file(filename+".html")

@app.route('/download/<type>/<file>',methods=['GET'])
def downloadfile(file,type):

     if request.method == 'GET':
         print(file)
         if(type=='m'):
            mapfile=file+".html"
            return send_file(mapfile, as_attachment=True)
         else :
            resultfile="uploads\\"+file+".txt"
            return send_file(resultfile, as_attachment=True)



def format_datetime(value):
    print(value)
    tdelta = value - datetime.now()
    difference =babel.dates.format_timedelta(tdelta, add_direction=True, locale='en_US')
    return difference

app.jinja_env.filters['datetime'] = format_datetime

if __name__ == "__main__":
    app.run(host='0.0.0.0')



