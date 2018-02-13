import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurements_table
Station = Base.classes.stations_table
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
    return ("Available Routes:<br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/stations<br/> \
            /api/v1.0/tobs<br/> \
            /api/v1.0/start<br/> \
            /api/v1.0/startAndEnd")

"""Query for the dates and temperature observations from the last year.
Convert the query results to a Dictionary using date as the key and tobs as the value.
Return the json representation of your dictionary."""
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement).filter(Measurement.date.between('2016-08-23', '2017-08-23'))
    tobs_lastyear = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["tobs"] = result.tobs
        tobs_lastyear.append(tobs_dict)
    return jsonify(tobs_lastyear)

"""Return a json list of stations from the dataset."""
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station)
    stationslist = []
    for result in results:
        stationslist.append(result.station)
    return jsonify(stationslist)

"Return a json list of Temperature Observations (tobs) for the previous year"
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement).filter(Measurement.date.between('2016-08-23', '2017-08-23'))
    tobs_lastyear = []
    for result in results:
        tobs_lastyear.append(result.tobs)
    return jsonify(tobs_lastyear)

"""/api/v1.0/<start> 
Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
@app.route("/api/v1.0/start")
def start():
    startDate=request.args.get('startDate', default = '2010-02-28' )
    results= session.query(func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs),\
                            func.max(Measurement.tobs)).\
                            filter(Measurement.date >= startDate).first()
    tobs_stats = []
    for result in results:
        tobs_stats.append(result)
    return jsonify(tobs_stats)

"""/api/v1.0/<start> and /api/v1.0/<start>/<end>
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
@app.route("/api/v1.0/startAndEnd")
def startAndEnd():
    startDate=request.args.get('startDate', default = '2015-02-28')
    endDate=request.args.get('endDate', default = '2017-02-28')
    results= session.query(func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs),\
                            func.max(Measurement.tobs)).\
                            filter(Measurement.date.between (startDate, endDate)).first()
    tobs_stats = []
    for result in results:
        tobs_stats.append(result)
    return jsonify(tobs_stats)


if __name__ == '__main__':
    app.run(debug=True)