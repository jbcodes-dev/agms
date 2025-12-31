from flask import Flask, render_template, request
import sys

# add other project files to path
sys.path.append("/home/jakebrown/final-year-project/src/main/")

import dbhandler

# create flask object
app = Flask(__name__)

# create database handler object
DBHandler = dbhandler.DBHandler("/home/jakebrown/final-year-project/src/database/database.db")

# index page
@app.route("/")
def index():
    rows = DBHandler.get_data("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1")

    data = []

    for item in rows:
        for subItem in item:
            data.append(subItem)
            
    temperature = data[1]
    humidity = data[2]
    time = str(data[3])

    template_data = {
            'temperature': temperature,
            'humidity': humidity,
            'time': time
        }

    return render_template("index.html", **template_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

