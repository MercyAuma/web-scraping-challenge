# Import Libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create Flash App
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Default Route: Retrive a record from Mongo db mars_facts db and display
@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)

# Scrape Route: execute scrape() function in screpe_mars.py file, store the returned dictionary in Mongo db
@app.route("/scrape")
def scrape():
    listings = mongo.db.listings
    listings_data = scrape_mars.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

    