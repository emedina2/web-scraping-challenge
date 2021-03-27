from flask import Flask, render_template, redirect
import scrape_mars 
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)
collection = mongo.db.mars_data


@app.route("/")
def home():
    mars_data = collection.find()
    mars_table = scrape_mars.get_mars_table()
    return render_template('index.html', mars_data = mars_data, table_data = mars_table)



@app.route("/scrape")
def scrape():
    scrape_mars.scrape()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)