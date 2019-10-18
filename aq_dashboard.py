from flask import Flask, render_template, request, redirect, url_for
import openaq_py
from get_data import *
from flask_sqlalchemy import SQLAlchemy
import pygal




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(30), nullable=False)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'

def populate_data(city):
    try:
        User.query.filter(User.name == city).one()
    except:
        api = openaq_py.OpenAQ()
        status, body = api.measurements(city=city, parameter='pm25')
        li = [(city,i['date']['utc'], i['value']) for i in body['results']]
        for i in li:
            put = Record(city=i[0], datetime=str(i[1]), value=i[2])
            DB.session.add(put)
        DB.session.commit()

@app.route('/')
def root():
    """Base view."""
    #li = data_grab()
    lii, parameter = drop_downs()
    return render_template('home.html', li=[('Los Angeles','Los Angeles')], parameter=parameter)
@app.route('/add/<name>')
def add(name):
    name = name.replace('-',' ')
    populate_data(name)
    return(redirect('/'))


@app.route('/dash/')
def dash():
    city = request.args.get('city')
    parameter = request.args.get('parameter')
    if "8" in city:
        city = city.replace("8", " ")
    res = data_grab(city, parameter)
    line_chart = pygal.Line()
    line_chart.x_labels = [i[0] for i in res]
    line_chart.add(parameter, [i[1] for i in res])

    graph_data = line_chart.render()
    return(render_template('graph.html',graph_data = graph_data))



@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'

if __name__ == '__main__':
    app.run(debug=True)
