# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time
import os




def init_browser():
    """ Connects path to chromedriver """
    
    executable_path = {'executable_path': 'C:\Users\Mercy\Downloads\chromedriver'}
    return Browser("chrome", **executable_path, headless=True)



def scrape():
    # browser = init_browser()
    browser=Browser('flask', app=app)
    listings = {}

    # URL of page to be scraped

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html'
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')


 
 
    # pull latest news title and paragrapgh
    slide_elem = news_soup.select_one('ul.item_list li.slide')
    title  = slide_elem.find('div', class_='content_title').text

    paragraph  = slide_elem.find('div', class_='article_teaser_body').text

    print('-----------------------------------------------------------------------------')
    print('News_title = '+title)
    print('')
    print('News_p = '+paragraph)
    print('-----------------------------------------------------------------------------')
    
    listings["Latest news tiles: "] = title
    listings["Latest news summary: "] = paragraph
       

    # # task 2
    image_url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(image_url)

    time.sleep(1)

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')


    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()   

    # return image
    
    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    img = image_soup.select_one("figure.lede a img").get("src")
    featured_image_url = 'https://www.jpl.nasa.gov/' + img
    print(featured_image_url)
    listings["featured_image_url: "] = featured_image_url

    # # task 3
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)


    twitter_response = requests.get(twitter_url)
    twitter_soup = BeautifulSoup(twitter_response.text, 'lxml')

    
    twitter_result = twitter_soup.find('div', class_='js-tweet-text-container').text.strip()
    #print(results_tweets)

     listings["final mars weather: "] = twitter_result

    # task 4
    #   scrape the table containing facts about the planet including Diameter, Mass, etc
    space_data = pd.read_html('https://space-facts.com/mars/')[0]
    space_data.columns=['Description','Value']
    space_data.set_index("Description",inplace=True)

    time.sleep(1)

    # Export pandas df to html script
    marsfacts = space_data.to_html()
    marsfacts.replace("\n", "")
    final_table=space_data.to_html('marsfacts.html')


    listings["final_table"] = final_table

    # # task 5
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    time.sleep(1)

    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'lxml')
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
 