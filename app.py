import pandas as pd
import numpy as np
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

base = automap_base()

base.prepare(engine, reflect=True)

measurements_table = base.classes.measurements

stations_table = base.classes.stations

session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():

    start_date = dt.date(2016, 8, 23)
    end_date = dt.date(2017, 8, 23)

    precipitation = session.query(measurements_table.date, measurements_table.prcp)\
    .filter(measurements_table.date >= start_date)\
    .filter(measurements_table.date <= end_date).all()
    
    #professions = dict([ (p.name, p.profession) for p in people ])
    precip_dict = dict([ (i.date, i.prcp) for i in precipitation ])
    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(stations_table.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    start_date = dt.date(2016, 8, 23)
    end_date = dt.date(2017, 8, 23)

    results = session.query(measurements_table.tobs)\
        .filter(measurements_table.station == 'USC00519281')\
        .filter(measurements_table.date >= start_date)\
        .filter(measurements_table.date <= end_date).all()

    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

@app.route("/api/v1.0/temp/<start>")
def start(start=None):

    sel = [func.min(measurements_table.tobs), func.avg(measurements_table.tobs), func.max(measurements_table.tobs)]

    results = session.query(*sel).filter(measurements_table.date >= start).all()
    temp_list = list(np.ravel(results))
    return jsonify(temp_list)

@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start=None, end=None):

    sel = [func.min(measurements_table.tobs), func.avg(measurements_table.tobs), func.max(measurements_table.tobs)]

    results = session.query(*sel).filter(measurements_table.date >= start).filter(measurements_table.date <= end).all()
    temp_list = list(np.ravel(results))
    return jsonify(temp_list)


if __name__ == '__main__':
    app.run()