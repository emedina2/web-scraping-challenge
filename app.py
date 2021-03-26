from flask import Flask, render_template
from scrape_mars 
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
@app.route("/")
def home():
    test_data = mongo.db.collection.find_one()
    return render_template(index.html, test = test_data)

@app.route("/scrape")
def scrape():
    scrape_mars.scrape()
    return redirect("/")