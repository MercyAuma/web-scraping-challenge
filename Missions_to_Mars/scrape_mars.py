# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time
import os


def init_browser():
    """ Connects path to chromedriver """
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
listings = {}

def scrape_News():
    
    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser = init_browser()
    browser.visit(news_url)
    time.sleep(3)
    news_response = requests.get(news_url)

   # Create BeautifulSoup object; 
    news_soup = bs(news_response.text, 'lxml')
    try:
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

    except AttributeError as e:
        return(e)
             
    finally:
        browser.quit()

    # task 2
def scrape_Weather():

        twitter_url = 'https://twitter.com/marswxreport?lang=en'
        twitter_response = requests.get(twitter_url)
        twitter_soup = bs(twitter_response.text,  'lxml')
        try:
            twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')
            mars_weather=twitter_result.text.strip()
    
        
        #store results into a dictionary listings
            listings["marsweather"] = mars_weather

        except AttributeError as e:
            print(e)
             
   

    # # task 3
def scrape_Image():
    # Call on chromedriver function to use for splinter
    browser = init_browser()

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(image_url)

    time.sleep(1)
    try:
        browser.click_link_by_partial_text('FULL IMAGE')
        image_html = browser.html

        image_soup = bs(image_html, "html.parser")
        
        featured_image = image_soup.select_one(".carousel_item").get("style")
        featured_image = featured_image.split("\'")[1]
        featured_image_url = f'https://www.jpl.nasa.gov{featured_image}'
        
        # Store url to dictionary
        listings["featured_image_url"] = featured_image_url
    except AttributeError as e:
        print(e)
    finally:
        browser.quit()

    # task 4
def scrape_Facts():
    browser = init_browser()
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(1)
    try:
        facts = pd.read_html(facts_url)
        mars_df = facts[0]
        mars_df.columns = ['Description', 'Value']
        mars_df.set_index('Description', inplace=True)

        mars_facts = mars_df.to_html()
        mars_facts.replace("\n","")
        mars_df.to_html('mars_facts.html')
        
        listings['mars_facts'] = mars_facts

        print('Mars Facts:'+ mars_facts)
        
    except AttributeError as e:
        print(e)

    finally:
        browser.quit()
        
    #task 5
def scrape_Hemispheres():
    # Call on chromedriver function to use for splinter
    browser = init_browser()
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(2)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"
    try:
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
            time.sleep(2)
            
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
    except AttributeError as e:
        print(e)

def scrape():                                     
    
    scrape_News()
    scrape_Weather()
    scrape_Image()
    scrape_Facts()
    scrape_Hemispheres()    
    return listings
 