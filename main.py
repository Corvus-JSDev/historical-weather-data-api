from flask import Flask, render_template
import os
from dotenv import load_dotenv
# load_dotenv()
# ENV = os.getenv("ENV")

app = Flask(__name__)


# When the user visits the site the index.htlm file will be shown
@app.route("/")
def home():
	return render_template("index.html")

@app.route("/api/v1/<station>/<date>")
def about(station, date):
	# return render_template("about.html")
	temp = 50
	return {
		"station": station,
		"date": date,
		"temp": temp
	}

app.run(debug=True, port=5000)


