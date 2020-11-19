import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
quant = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/passengers"      
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    # Query
    results = session.query(quant.date, quant.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    output = list(np.ravel(results))

    return jsonify(output)


@app.route("/api/v1.0/stations")
def stations():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query
    results = session.query(station.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    output = list(np.ravel(results))

    return jsonify(output)


@app.route("/api/v1.0/tobs")

def tobs():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data."""
    # Query 
    results = session.query(quant.date, quant.tobs).filter(quant.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    output = list(np.ravel(results))

    return jsonify(output)


@app.route("/api/v1.0/<start>")

def start_param(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
  """calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""  
  # Query 
    prcp = session.query(quant.date,func.min(quant.tobs),func.avg(quant.tobs), func.max(quant.tobs)).\
                    filter(quant.date >= start).\
                    group_by(quant.date).all()

    session.close()

    # Convert list of tuples into normal list
    output = list(np.ravel(results))
    
    return jsonify(output)




@app.route("/api/v1.0/<start>/<end>")

def duration_param(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(quant.date, quant.prcp).all()

    prcp = session.query(quant.date,func.min(quant.tobs),func.avg(quant.tobs), func.max(quant.tobs)).\
                    filter(quant.date >= start & quant.date <= end).\
                    group_by(quant.date).all()

    session.close()

    # Convert list of tuples into normal list
    output = list(np.ravel(results))

    return jsonify(output)


    

if __name__ == '__main__':
    app.run(debug=True)
