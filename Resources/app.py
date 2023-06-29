


#################################################
# Import the necessary dependencies
from sqlalchemy import create_engine, MetaData, Table, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
import datetime as dt
import os
# Create the engine to connect to the SQLite database file
database_path = os.path.join("resources", "hawaii.sqlite")

# Create the engine and reflect the database
engine = create_engine(f"sqlite:///{database_path}")
# Reflect the existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table in variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session (link) from Python to the database
session = Session(engine)



#################################################
# Flask Setup
#################################################
# Create a Flask app instance
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define the homepage route
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).all()

    return jsonify(precipitation_data)

# Define the stations route
@app.route("/api/v1.0/stations")


def stations():
    station_count = session.query(func.count(Station.station)).scalar()
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

# Print the stations and their counts in descending order
#for station, count in active_stations:
  #  print(f"Station: {station}, Count: {count}")
 #   
    return jsonify(active_stations)

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    most_active_station = active_stations[0][0]
    temperature_data = session.query(Measurement.tobs).\
    filter(Measurement.station == most_active_station).\
    filter(Measurement.date >= one_year_ago).all()

    return jsonify(temperature_data)

# Define the start date route
#@app.route("/api/v1.0/<start>")
#def start_date(start):
    # Place your code for retrieving and processing temperature statistics for a specified start date here
   
    #return jsonify(temperature_stats)

# Define the start and end date route

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
    return jsonify(temperature_stats)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
