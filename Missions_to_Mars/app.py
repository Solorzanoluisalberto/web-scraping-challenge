from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    mars_scrap = mongo.db.mars_scrap.find_one()
    return render_template('index.html', mars_scrap=mars_scrap)

@app.route('/scrape')
def scrape():
    mars_scrap = mongo.db.mars_scrap
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
