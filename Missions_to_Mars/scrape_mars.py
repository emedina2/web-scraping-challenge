# Dependencies
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs

def get_mars_table():
    #Get Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_data = pd.read_html(mars_facts_url)
    #convert to html table
    clean_table = mars_data[0].set_index([0])
    clean_table.index.name="Description"
    clean_table = clean_table.rename(columns={1: ""})
    mars_data_table =clean_table.to_html()
    mars_data_table
    clean_table
    return mars_data_table

def scrape():
   
    mars_facts_url = 'https://space-facts.com/mars/'
    response = requests.get(mars_facts_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    mars_news_scraped = soup.find('div', id = 'facts' )
    headline = mars_news_scraped.find('strong').text
    mars_list = mars_news_scraped.find_all('li')[0]
    news_text =  mars_list.next_sibling.text
    
     #open browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    #Get Featured Image
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    featured_image = image_soup.find('div', class_ = 'floating_text_area')
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured_image.a['href']
    #Get Mars Facts
    mars_data = pd.read_html(mars_facts_url)
    #convert to html table
    mars_data_table = mars_data[0].to_html()

    mars_db_data = {
        'headline' : headline,
        'headline_text':news_text,
        'featured_image_url' : featured_image_url
    }
    #Connect to PyMongo/MongoDB to store data
    conn = "mongodb://localhost:27017"
    client = MongoClient(conn)
    db = client.mars_db
    collection = db.mars_data
    collection.delete_many({})
    collection.update({},mars_db_data, upsert=True)
    
    #Grab Hemisphere links
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemisphere_image_url = {}
    short_url = 'https://astrogeology.usgs.gov/'
    short_img_url = 'https://astrogeology.usgs.gov'
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    hemisphere_items = hemispheres_soup.find('div', class_='collapsible results').find_all('div', class_='item')
    for hem_url in hemisphere_items:
        browser.visit(short_url + hem_url.a['href'])
        hemisphere_body = bs(browser.html, 'html.parser').find('body')
        image_title = hemisphere_body.find('div', class_='content').find('h2', class_='title').text
        image_url = hemisphere_body.find('img', class_='wide-image')['src']
        hemisphere_image_url['title'] =  image_title
        hemisphere_image_url['img_url'] = short_img_url + image_url
        collection.insert_one(hemisphere_image_url.copy())
    browser.quit()
    
  
    

    