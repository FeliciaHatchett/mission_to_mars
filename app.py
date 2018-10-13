
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    # render template is looking for a folder called template
    return render_template('index.html', mars=mars) 

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return "scraping successful"

if __name__ == "__main__":
    app.run(debug=True)