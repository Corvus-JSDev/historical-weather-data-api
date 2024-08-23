from flask import Flask, render_template
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
# load_dotenv()
# ENV = os.getenv("ENV")

app = Flask(__name__)


available_stations = pd.read_csv("data_small/stations.txt", skiprows=17)
available_stations = available_stations[["STATION ID", "STATION NAME                                 "]]

# When the user visits the site the index.htlm file will be shown
@app.route("/")
def home():
	return render_template("index.html", data=available_stations.to_html())


@app.route("/api/v1/<station>/<date>")
def temp_data(station, date):
	df = pd.read_csv(f"data_small/TG_STAID{station:>06}.txt", skiprows=20, parse_dates=["    DATE"])
	df["TG_0"] = df["   TG"].mask(df["   TG"] == -9999, np.nan) / 10

	celsius = df.loc[df["    DATE"] == date]["TG_0"].squeeze() / 10
	fahrenheit = (celsius * 1.8) + 32

	celsius = celsius if not np.isnan(celsius) else "N/A"
	fahrenheit = fahrenheit if not np.isnan(fahrenheit) else "N/A"

	return {
		"station": station,
		"date": {
			"raw": date,
			"formated_date": f"{date[:4]}-{date[4:6]}-{date[6:]}"
		},
		"temp": {
			"celsius": celsius,
			"fahrenheit": fahrenheit,
		}
	}



@app.route("/api/v1/<station>")
def station_data(station):
	df = pd.read_csv(f"data_small/TG_STAID{station:>06}.txt", skiprows=20)
	df["REAL_TEMP"] = df["   TG"].mask(df["   TG"] == -9999, np.nan) / 10

	return render_template("station-data.html", data=df.to_html())


@app.route("/api/v1/year/<station>/<year>")
def yearly_data(station, year):
	df = pd.read_csv(f"data_small/TG_STAID{station:>06}.txt", skiprows=20)
	df["    DATE"] = df["    DATE"].astype(str)

	result = df[df["    DATE"].str.startswith(str(year))]

	return render_template("station-data.html", data=result.to_html())





app.run(debug=True, port=5000)


