# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of dates and precipitation"""
    # Query for the last 12 months of precipitation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a dictionary
    precipitation_dict = {}
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    stations_data = session.query(Station.station).all()
    stations_list = list(np.ravel(stations_data))
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations for the previous year"""
    # Query for the last 12 months of temperature observation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)
    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a dictionary
    temperature_dict = {}
    for date, tobs in temperature_data:
        temperature_dict[date] = tobs
    
    return jsonify(temperature_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return a list of minimum, average, and maximum temperatures for a given start date"""
    # Query for the minimum, average, and maximum temperatures for a given start date
    start_date_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    # Convert the query results to a list
    start_temps_list = list(np.ravel(start_date_temps))