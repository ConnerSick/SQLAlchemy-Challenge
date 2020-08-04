import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///./hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    prior_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= prior_year_date).all()
    
    precip_results = {date: prcp for date, prcp in results}
 
    return jsonify(precip_results)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    
    station_results = list(np.ravel(results))
    return jsonify(station_results)

    
@app.route("/api/v1.0/tobs")
def tobs():    
    prior_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prior_year_date).all()
 
    tobs_results = list(np.ravel(results))
    
    return jsonify(tobs_results)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def startrange(start=None,end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        temps = list(np.ravel(results))
        
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    
    return jsonify(temps)

    
if __name__ == '__main__':
    app.run()