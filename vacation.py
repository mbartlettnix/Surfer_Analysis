from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

import datetime as dt
import numpy as np
import pandas as pd



# SQL Alchemy Setup#############
engine = create_engine("sqlite:///hawaii.sqlite")
inspector = inspect(engine)
Base = automap_base()
Base.prepare(engine=engine, reflect=True)    

stations = Base.classes.stations
measurement = Base.classes.measurement
# 
session = Session(bind=engine)
# ####################


app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("Welcome to the Hawaii Surfer's Analysis site<br/><br/>"
    		"Here are the available end points:<br/>"
    		"/api/v1.0/precipitation<br/>"
    		"/api/v1.0/stations<br/>"
    		"/api/v1.0/tobs<br/>"
    		"/api/v1.0/*enter start date in Y-m-d format*<br/>"
    		"/api/v1.0/*enter start date in Y-m-d format*/*enter end date in Y-m-d format*<br/>")



@app.route("/api/v1.0/precipitation")
def precip():
	# Query for the dates and precip observations from the last year.
	# Convert the query results to a Dictionary using date as the key and precip as the value.
	# Return the json representation of your dictionary.
	print("Server received request for precip page...")
	prcp = pd.DataFrame(session.query(measurement.date,measurement.prcp).\
	filter(measurement.date >= '2016-01-01', measurement.date < '2017-01-01').all())
	prcp = prcp.set_index('date')
	prcp =prcp.to_dict()
	
	return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stats():
     # Return a json list of stations from the dataset.
     print("Server received request for station page...")
      
     returns = session.query(stations.name).all()
     return jsonify(returns)
     

@app.route("/api/v1.0/tobs")
def tobsy():
	# Return a json list of Temperature Observations (tobs) for the previous year
     print("Server received request for tobs page...")
     returns = session.query(measurement.date,measurement.tobs).filter(
       measurement.date >= '2016-01-01', measurement.date < '2017-01-01').all()
     return jsonify(returns)


# Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def temp_input(start):
	def starttemp(start_date):
		print("Server received request for start page...")
		data = pd.DataFrame(session.query(measurement.tobs).\
		filter(measurement.date >= start_date).all())

		avg = round(data['tobs'].mean())
		low = data['tobs'].min()
		high = data['tobs'].max()
		return avg,low,high

	average,minimum,maximum = starttemp(start)
	dictionary = {"Minimum_Temp":str(minimum),"Average_Temp": str(average),"Max_Temp":str(maximum)}
	return jsonify(dictionary)


@app.route("/api/v1.0/<start>/<end>")
# create first function to gather inputs from user in address line then pushes them into nested dunction
def temp_input_end(start,end):
	def calc_temps(start_date,end_date):
		print("Server received request for start/end page...")
		data = pd.DataFrame(session.query(measurement.tobs).\
		filter(measurement.date >= start_date, measurement.date < end_date).all())

		avg = round(data['tobs'].mean())
		low = data['tobs'].min()
		high = data['tobs'].max()
		return avg,low,high

	average,minimum,maximum = calc_temps(start, end)
	dictionary = {"Minimum_Temp":str(minimum),"Average_Temp": str(average),"Max_Temp":str(maximum)}
	return jsonify(dictionary)




if __name__ == "__main__":
    app.run(debug=True)
