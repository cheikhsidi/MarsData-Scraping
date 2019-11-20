from flask import Flask, jsonify, render_template
import pymongo
import scrape_mars

app = Flask(__name__)


# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.Mars_db

# Drops collection if available to remove duplicates
db.Mars_db.drop()

# Creates a collection in the database and inserts two documents
#db.Mars.insert_one()

# create route that renders index.html template


@app.route("/scrape/")
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    Mars_db.db.collection.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route("/")
def index():
    # Find one record of data from the mongo database
    Mars_data = Mars_db.db.collection.find_one()

    # Return template and data
    return render_template("index.html", vacation=Mars_data)

if __name__ == "__main__":
    app.run(debug=True)
