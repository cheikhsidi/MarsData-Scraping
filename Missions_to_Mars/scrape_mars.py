#Importing the dependencies
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import datetime as dt
from splinter import Browser
import tweepy
import api_keys


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser = init_browser()
    mars = []
    data = {}
    
    # News URL
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    article = soup.find("div", class_='list_text')
    # News Title
    news_title = article.find("div", class_="content_title").text
    #news_title = soup.find_all('div', class_='content_title')[0].find('a').text.strip()
    news_p = article.find("div", class_="article_teaser_body").text
    data['news_title'] = news_title
    data['news_paragraph'] = news_p

    # Feutured Image of Mars
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    featured_image = soup.find("img", class_="thumb")
    # fetching the image
    featured_image = featured_image["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image
    data['featured_image'] = featured_image_url

    # Mars Weather
    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(api_keys.api_key, api_keys.api_secret)
    auth.set_access_token(api_keys.token_access, api_keys.token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    end_point = "MarsWxReport"
    tweet = api.user_timeline(end_point, count=1)
    mars_weather = ((tweet)[0]['text'])
    data['mars_weather'] = mars_weather

    # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_dt = pd.read_html(facts_url)[0]
    mars_df = pd.DataFrame(mars_dt)
    mars_df.columns = ["Description", "Value"]
    #mars_df = mars_df.set_index("Description")
    mars_facts_html = mars_df.to_html(index=True, header=True)
    mars_facts_html = mars_facts_html.replace('\n', '')
    data['mars_facts'] = mars_facts_html

    # Mars Hemispheres
    hemi_spheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_spheres_url)
    html = browser.html
    soup = bs(html, "html.parser")

    products = soup.find("div", class_="result-list")
    hemispheres = products.find_all("div", class_="item")
    mars_hmspr = []
    n = 1
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + link
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        dt = soup.find("div", class_="downloads")
        image_url = dt.find("a")["href"]
        dict_ = {f"title_{n}": title, f"img_url_{n}": image_url}
        n +=1
        #mars_hmspr.append(dict_)
        mars.append(dict_)
    mars.append(data)

    # Close the browser after scraping
    browser.quit()
    print(mars)
    return mars
