from flask import Flask, render_template
import os
from dotenv import load_dotenv
# load_dotenv()
# ENV = os.getenv("ENV")

app = Flask("Weather Data Website")


# When the user visits the site the index.htlm file will be shown
@app.route("/")
def home():
	return render_template("index.html")

app.run(debug=True)


