
# coding: utf-8

# # Web Scraping with BeautifulSoup4

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup


# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url="https://mars.nasa.gov/news/"
browser.visit(url)


# In[4]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


#collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.
news_title = soup.find('div', class_="content_title").find('a').text
news_p = soup.find('div', class_="article_teaser_body").text


# In[6]:


# Visit the url for JPL Featured Space Image
mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(mars_url)


# In[7]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[8]:


#Use splinter to navigate the site and find the image url for the current Featured Mars Image 
#and assign the url string to a variable called `featured_image_url`
featured_image = soup.find('div', class_="default floating_text_area ms-layer").find('a')["data-fancybox-href"]
featured_image_url= "https://www.jpl.nasa.gov" + featured_image
featured_image_url


# In[63]:


# Visit the Mars Weather twitter account
weather_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(weather_url)


# In[64]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[84]:


#Locate weather tweets and iterate through tweets to find original Mars Weather content to append to a list
results = []
for result in soup.find_all('div', attrs={"data-name": "Mars Weather"}):
    for p in result.find_all('p'):
        results.append(p.text)

#Use tweet at index 1 containing latest weather report
mars_weather=results[1]
mars_weather


# In[12]:


#import Pandas
import pandas as pd


# In[13]:


# use Pandas to scrape the table containing facts about the planet
facts_url = "http://space-facts.com/mars/"
tables = pd.read_html(facts_url)
tables


# In[14]:


img_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(img_url)


# In[15]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[61]:


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


# In[62]:


hemisphere_image_urls


# In[ ]:


# c_hem = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"
# sc_hem = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"
# sy_hem = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"
# v_hem = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"

# images= [c_hem, sc_hem, sy_hem, v_hem]

