from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scraper

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    scrape = mars_scraper.scrape()
    table = scrape[1]
    mars = mongo.db.mars.find_one()
    hemi = mongo.db.hemi.find_one()

    return render_template("index.html", hemi=hemi, mars=mars, table=table)


@app.route("/scrape")
def scraper():
    hemi = mongo.db.hemi
    mars = mongo.db.mars
    scrape_data = mars_scraper.scrape()
    mars_data = scrape_data[0]
    hemi_data = scrape_data[2]
    hemi.update({}, mars_data, upsert=True)
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
