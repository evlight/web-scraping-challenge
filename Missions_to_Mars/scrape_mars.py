#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time



def scrape_info():

    browser=Browser('chrome')
    mars={}
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')
    news_title=soup.find('div',class_="content_title").a.text
    news_title 
    mars["news_title"]=news_title


    paragraph=soup.find('div', class_="article_teaser_body").text
    paragraph
    mars["paragraph"]=paragraph


    saturn_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(saturn_url)
    time.sleep(2)


    click_image=browser.find_by_id("full_image")
    click_image.click()
    time.sleep(2)


    links_found1 = browser.find_link_by_partial_text('more info')
    print(links_found1)
    links_found1.click()
    time.sleep(5)



    soup = BeautifulSoup(browser.html, 'html.parser')
    results=soup.find("figure",class_= "lede")
    featured_image_url="https://www.jpl.nasa.gov"+results.a.img["src"]
    featured_image_url
    mars["featured_image_url"]=featured_image_url


    mars_weather=[]
    tweeter_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(tweeter_url)
    response = requests.get(tweeter_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    results=soup.find_all('div', class_="js-tweet-text-container")
    for result in results:
        mars_weather.append(result.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text)
    mars["weather"]= mars_weather[0]
    mars["weather"]



    url="http://space-facts.com/mars/"
    df=pd.read_html(url)[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    df

    df.to_html()

    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        time.sleep(1)
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        time.sleep(1)
    mars["hemisphere"]=hemisphere_image_urls
    mars["hemisphere"]

    return mars 
if __name__ == "__main__":
    print(scrape_info())
    




