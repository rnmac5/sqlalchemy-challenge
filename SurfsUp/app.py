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
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")
 
 
@app.route("/api/v1.0/percipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    """Return a list of all percipitation"""
    # Query all passengers
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
 
 
    # Convert list of tuples into normal list
    all_prcp = []
    for date,prcp in result:
        weather_dict = {}
        weather_dict["date"] = date
        weather_dict["prcp"] = prcp
        all_prcp.append(weather_dict) 
    
    return jsonify(all_prcp)
 
 

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    stations = session.query(Station.station).all()
 
    session.close()
 
    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = list(np.ravel(stations))
 
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    """Return a list of all passenger names"""
    # Query all passengers
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= year_ago).all()
 
    session.close()
 
    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(tobs))
 
    return jsonify(all_tobs)





if __name__ == '__main__':
    app.run(debug=True)








