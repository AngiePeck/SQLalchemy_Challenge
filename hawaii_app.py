import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


#Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def home():
    return (
        f"Welcome to Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation/<date, value><br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate/start<br/>"
        f"/api/v1.0/daterange/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation/<date>")
#<date>"
def precipitation(date):
    session = Session(engine)
            #session.query(func.min(Measurement.tobs)).filter(Measurement.station == 'USC00519281').first()
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date == date).all()

    session.close()

    prcp_specific_date = list(np.ravel(results))

    return jsonify(prcp_specific_date)
    
    #"Converts query results to a dictionary using date as the key and prcp as the value, returns the JSON representation of your dictionary"


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_list = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(station_list))
    return jsonify(stations)
    #"Returns a JSON list of stations from the dataset."

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    temps_active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()

    session.close()

    temps_active = list(np.ravel(temps_active_station))

    return jsonify(temps_active)
    #"Query the dates and temp observations of the most active station returns the JSON list of tobs for previous year"


@app.route("/api/v1.0/startdate/<start>")
def startdate(start):
    session = Session(engine)

    temp_data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').filter(Measurement.date > start).all()
    #return "calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date"

    session.close()

    temp_data_list = list(np.ravel(temp_data))

    return jsonify(temp_data_list)

@app.route("/api/v1.0/daterange/<start>/<end>")
def daterange(start, end):
    session = Session(engine)

    temp_range = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').filter(Measurement.date.between(start, end)).all()

    session.close()

    temp_range_list = list(np.ravel(temp_range))

    return jsonify(temp_range_list)
    #"start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive"

if __name__ == "__main__":
    app.run(debug=True)
