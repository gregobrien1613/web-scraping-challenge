from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    hemispheres = {}
    hemi = {}
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('div', class_='list_text')

    for article in articles:

        title = article.find('div', class_='content_title').text

        body = article.find('div', class_='article_teaser_body').text

        hemispheres["news_title"] = title
        hemispheres["news_body"] = body


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.find_by_xpath("//*[@id='full_image']").click()
    browser.find_by_xpath("//*[@id='fancybox-lock']/div/div[2]/div/div[1]/a[2]").click()
    browser.find_by_xpath("//*[@id='page']/section[1]/div/article/figure/a/img").click()
    img_url = browser.url

    hemispheres["main_img"] = img_url

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(2)
    temp = browser.find_by_xpath("//*[contains(text(),' low ')]").text
    hemispheres["weather"] = temp

    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)
    table

    df = table[0]
    df.columns = ["Stat", "Info"]
    df.reset_index(drop=True, inplace=True)
    df = df.to_html()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_list = soup.find_all('a', {'class': "itemLink product-item"})
    browser.visit(url)

    for link in link_list:
        hemi["title"] = link.find('h3').text
        browser.visit("https://astrogeology.usgs.gov" + link['href'])
        browser.find_by_xpath("//*[@id='wide-image-toggle']").click()
        hemi["img_url"] = browser.find_by_xpath("//img[@class='wide-image']")['src']
        browser.visit(url)
        print(hemi["img_url"])
    browser.quit()

    return hemispheres, df, hemi
