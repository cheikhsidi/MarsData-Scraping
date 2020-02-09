from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_db"
mongo = PyMongo(app)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    Mars = mongo.db.Mars_data
    Mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    Mars_dict = dict((key, d[key]) for d in Mars_data for key in d)
    Mars.update({}, Mars_dict, upsert=True)
    #mongo.db..update({}, d, upsert=True)

    # Redirect back to home page
    return redirect("/")

# create route that renders index.html template
@app.route("/")
def index():
    # Find one record of data from the mongo database
    Mars_data = mongo.db.Mars_data.find_one()

    # Return template and data
    return render_template("index.html", Mars_data=Mars_data)

if __name__ == "__main__":
    app.run(debug=True)
