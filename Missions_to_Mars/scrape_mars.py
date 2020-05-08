# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time
import requests

import os


def init_browser():
    """ Connects path to chromedriver """
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    listings = {}

    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    news_response = requests.get(news_url)

   # Create BeautifulSoup object; 
    news_soup = bs(news_response.text, 'lxml')

   # pull latest news title and paragrapgh
    results = news_soup.find('div', class_='features')
    title = results.find('div', class_='content_title').text
    paragraph = results.find('div', class_='rollover_description').text



    # print('-----------------------------------------------------------------------------')
    # print('News_title = '+title)
    # print('')
    # print('News_p = '+paragraph)
    # print('-----------------------------------------------------------------------------')
    
    #store results into a dictionary listings
    listings["Latest_news_titles"] = title
    listings["Latest_news_summary"] = paragraph
       

    # # task 2

    # Call on chromedriver function to use for splinter
    browser = init_browser()

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(image_url)

    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    image_html = browser.html

    image_soup = bs(image_html, "html.parser")
    
    featured_image = image_soup.select_one(".carousel_item").get("style")
    featured_image = featured_image.split("\'")[1]
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image}'
    
    # Store url to dictionary
    listings["featured_image_url"] = featured_image_url

    # task 3
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    

    twitter_response = requests.get(twitter_url)
    twitter_soup = bs(twitter_response.text, 'lxml')

    
    twitter_result = twitter_soup.find('div', class_='js-tweet-text-container').text.strip()
   
    #store results into a dictionary listings
    listings["final mars weather: "] = twitter_result

    # task 4
    #scrape the table containing facts about the planet including Diameter, Mass, etc
    space_data = pd.read_html('https://space-facts.com/mars/')[0]
    space_data.columns=['Description','Value']
    space_data.set_index("Description",inplace=True)

    
    # Export pandas df to html script
    marsfacts = space_data.to_html()
    marsfacts.replace("\n", "")
    final_table=space_data.to_html('marsfacts.html')

    #store results into a dictionary listings
    listings["final_table"] = final_table

    #task 5
    # Call on chromedriver function to use for splinter
    
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    image_list = hemisphere_soup.find_all('div', class_='item')

    # Create list to store dictionaries of data
    hemisphere_image_urls = []

   # Loop through list of hemispheres and click on each one to find large resolution image
    for image in image_list:

        # Create a dicitonary to store urls and titles
        hemisphere_dict = {}
        
        # Find link to large image
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']

        # Visit the link
        browser.visit(link)

        # Wait 1 second 
        time.sleep(1)
        
        # Parse the html of the new page
        hemisphere_html2 = browser.html
        hemisphere_soup2 = bs(hemisphere_html2, 'lxml')

        # Find the title
        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        
        # Append to dict
        hemisphere_dict['title'] = img_title
    
        # Find image url
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        
        # Append to dict
        hemisphere_dict['url_img'] = img_url
        
        # Append dict to list
        hemisphere_image_urls.append(hemisphere_dict)
    
    # Store hemisphere image urls to dictionary
        listings['hemisphere_image_urls'] = hemisphere_image_urls

    
    return listings
 