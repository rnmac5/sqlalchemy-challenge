import numpy as np
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        f"<p>'start' and 'end' date should be in YYYY-MM-DD")
 
 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    """Return a list of all precipitation"""
    # Query all with the year ago date and precipitation
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
 
    session.close()

    # Convert list of tuples into normal list
    all_prcp = {date: prcp for date, prcp in result} 
    
    return jsonify(all_prcp)
 
 

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    # Query all stations
    stations = session.query(Station.station).all()
 
    session.close()
 
    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = list(np.ravel(stations))
 
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    """Return a list of all tobs"""
    # Query all tobs
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= year_ago).all()
 
    session.close()
 
    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(tobs))
 
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dates(start= None, end= None):
    #Create our session from Python
    session = Session(engine)

    #Set up the functions for min, avg and max
    select= [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #Query the functions
    if not end:
        final_result= session.query(*select).\
            filter(Measurement.date >= start).all()
        final_tobs= list(np.ravel(final_result))
        return jsonify(final_tobs)
    final_result= session.query(*select).\
        filter(Measurement.date >=start).\
        filter(Measurement.date <=end).all()
    final_tobs= list(np.ravel(final_result))
    return jsonify(final_tobs=final_tobs)

    

if __name__ == '__main__':
    app.run(debug=True)






