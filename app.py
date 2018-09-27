from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import datetime
import json
import babel
import teltonikaparser


app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class MyForm(FlaskForm):
    data = StringField('Raw Data', validators=[DataRequired()])




@app.route('/')
def hello():
    return "Hello World!"


@app.route("/")
def home():
    return ("Home")

@app.route('/teltonika/',methods=['GET', 'POST'])
def parseteltonika():
    form = MyForm()
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


def format_datetime(value):
    print(value)
    tdelta = value - datetime.now()
    difference =babel.dates.format_timedelta(tdelta, add_direction=True, locale='en_US')
    return difference

app.jinja_env.filters['datetime'] = format_datetime

if __name__ == "__main__":
    app.run(host='0.0.0.0')



