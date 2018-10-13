
# coding: utf-8

# # Web Scraping with BeautifulSoup4
from splinter import Browser
from bs4 import BeautifulSoup
import time

def initialize_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = initialize_browser()
    mars = {}
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #collect the latest News Title and Paragraph Text. 
    #Assign the text to variables that you can reference later.
    mars["news_title"] = soup.find('div', class_="content_title").find('a').text
    mars["news_p"] = soup.find('div', class_="article_teaser_body").text

    # Visit the url for JPL Featured Space Image
    mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    #and assign the url string to a variable called `featured_image_url`
    featured_image = soup.find('div', class_="default floating_text_area ms-layer").find('a')["data-fancybox-href"]
    mars["featured_image_url"]= "https://www.jpl.nasa.gov" + featured_image


    # Visit the Mars Weather twitter account
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Import re to scrape for tweets containing weather data
    import re
    mars_weather=soup.find(string=re.compile("Sol"))
    print(mars_weather) 



    #import Pandas
    import pandas as pd

    # use Pandas to scrape the table containing facts about the planet
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    table = df.to_html()
    table = table.replace('\n', '')

    mars['facts'] = table

    # Visit mars images
    img_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(img_url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    links = []
    titles = []
    for data in soup.find_all('div', class_='description'):
        for a in data.find_all('a'):
            link= a.get('href')
            link = "http://astropedia.astrogeology.usgs.gov/download" + link[11:] + ".tif/full.jpg"
            title= a.text
            title=title[:-9]
            links.append(link)
            titles.append(title)

    hemisphere_image_urls = []
   
    for link, title in zip(links, titles):
        post= {"title": title, "img_url": link}
        hemisphere_image_urls.append(post)
    
    mars["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    return mars




