from flask import Flask, request, jsonify
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import urllib.parse

app = Flask(__name__)

def scrape_flights(departure, destnation, startdate):
    driver = webdriver.Chrome()
    url = f'https://www.kiwi.com/us/search/results/{departure}/{destnation}/{startdate}/no-return'
    driver.get(url)
    popup_window = '//*[@id="cookies_accept"]'
    driver.find_element("xpath", (popup_window)).click()
    driver.execute_script('window.scrollBy(0,1700)')
    sleep(2)
    flight_rows = driver.find_elements("xpath", ('//*[@data-test="ResultCardWrapper"]'))
    
    lst_prices = []
    lst_time = []
    lst_airport = []
    for WebElement in flight_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        temp_price = elementSoup.find("div", {"data-test": "ResultCardPrice"})
        if temp_price is None:
            continue
        price = temp_price.find("span", {"class": "length-3"})
        if price is None:
            price = temp_price.find("span", {"class": "length-4"})
        if price is None:
            price = temp_price.find("span", {"class": "length-5"})
        lst_prices.append(price.text)

        temp_price = elementSoup.find_all("div", {"data-test": "TripTimestamp"})
        departure = temp_price[0].find("time")
        arrival = temp_price[1].find("time")
        lst_time.append(departure.text)
        lst_time.append(arrival.text)

        temp_airport = elementSoup.find_all("div", {"data-test": "ResultCardStopPlace"})
        departure_airport = temp_airport[0].find("div", {"data-test": "iataCode"})
        arrival_airport = temp_airport[1].find("div", {"data-test": "iataCode"})
        lst_airport.append(departure_airport.text)
        lst_airport.append(arrival_airport.text)

    driver.quit()
    return lst_prices, lst_time, lst_airport

def scrape_restaurants(destnation):
    driver = webdriver.Chrome()
    url = f'https://www.yelp.com/search?find_desc=Restaurants&find_loc={urllib.parse.quote(destnation)}'
    driver.get(url)
    driver.execute_script('window.scrollBy(0,4000)')
    sleep(5)
    restaurant_rows = driver.find_elements("xpath", ('//*[@data-testid="serp-ia-card"]'))
    restaurant_rows.pop(0)
    restaurant_rows.pop(0)
    
    restaurants = []
    ratings = []
    reviews = []
    tags = []
    for WebElement in restaurant_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        
        temp_restaurant = elementSoup.find("span", {"class": "css-1egxyvc"})
        if temp_restaurant is None:
            continue
        else:
            restaurant = temp_restaurant.find("a", {"class": "css-19v1rkv"})
            restaurants.append(restaurant.text)
        
        temp_rating = elementSoup.find("span", {"class": "css-gutk1c"})
        if temp_rating is None:
            ratings.append('NaN')
        else:
            ratings.append(temp_rating.text)
        
        temp_review_num = elementSoup.find("span", {"class": "css-8xcil9"})
        if temp_review_num is None:
            reviews.append('NaN reviews')
        else:
            reviews.append(temp_review_num.text)

        temp_tags = elementSoup.find_all("span", {"class": "css-11bijt4"})
        tags_text = [tag.text for tag in temp_tags]
        tags.append(tags_text)

    driver.quit()
    return restaurants, ratings, reviews, tags

@app.route('/api/flights', methods=['POST'])
def get_flight_information():
    departure = request.form.get('departure')
    destnation = request.form.get('destnation')
    startdate = request.form.get('startdate')

    lst_prices, lst_time, lst_airport = scrape_flights(departure, destnation, startdate)

    return jsonify({
        "flights": [
            {
                "price": lst_prices[i],
                "departure_time": lst_time[i * 2],
                "arrival_time": lst_time[i * 2 + 1],
                "departure_airport": lst_airport[i * 2],
                "arrival_airport": lst_airport[i * 2 + 1]
            } for i in range(len(lst_prices))
        ],
        "type" : "flights"
    })

@app.route('/api/restaurants', methods=['POST'])
def get_restaurant_information():
    destnation = request.form.get('destnation')
    restaurants, ratings, reviews, tags = scrape_restaurants(destnation)

    return jsonify({
        "restaurants": [
            {
                "name": restaurants[i],
                "rating": ratings[i],
                "reviews": reviews[i],
                "tags": tags[i]
            } for i in range(10)
        ],
        "type": "restaurants"
    })

if __name__ == '__main__':
    app.run(debug=True)