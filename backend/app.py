from flask import Flask, request, jsonify
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import urllib.parse
from openai import OpenAI


app = Flask(__name__)
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)
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
            ratings.append('')
        else:
            ratings.append(temp_rating.text)
        
        temp_review_num = elementSoup.find("span", {"class": "css-8xcil9"})
        if temp_review_num is None:
            reviews.append('')
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

@app.route('/api/text', methods=['POST'])
def get_text():
    departure = request.form.get('departure')
    destnation = request.form.get('destnation')
    startdate = request.form.get('startdate')

    arrivaldate = request.form.get('arrivaldate');
    numtraveler = request.form.get('numtraveler');
    text="Can you plan a trip based on all of these questions and answers:"+"Where would you like to go?"+destnation+"Where would you like to leave"+departure+"What time of month are you going?"+startdate+"What time of month are you returning?"+arrivaldate+"How many people in your group"+numtraveler+"Also can you plan this trip in this order: ONLY 1 Daily schedule with links for each activity and an estimated price for the activity for everyone(do not provide more than 1 itinerary on the output), ONE A packing list, after providing a daily activiy and packing list provide 10 hotel or airbnb reccomendation for the whole trip with links and lastly 10 reccomended reasturant locations for the whole trip based on the given information and location"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="gpt-3.5-turbo",
    )
    choice = chat_completion.choices[0]

    # Accessing the message attribute of the choice, which is a ChatCompletionMessage object
    message = choice.message

    # Accessing the content attribute of the message
    response_content = message.content
    return jsonify({
        "API":  response_content.strip(),


        "type": "Text"
    })
@app.route('/api/hotels', methods=['POST'])
def get_hotels():
    adults = request.form.get('numtraveler')
    d1 = request.form.get('startdate')
    d2 = request.form.get('arrivaldate')
    dest = request.form.get('destnation')
    
    url = f'https://www.hotels.com/Hotel-Search?adults={adults}&d1={d1}&d2={d2}&destination={dest}&endDate={d2}&sort=RECOMMENDED&startDate={d1}'
    
    driver = webdriver.Chrome()  # You need to set up the webdriver as needed
    driver.get(url)
    driver.execute_script('window.scrollBy(0,4000)')
    sleep(5)

    hotel_rows = driver.find_elements("xpath", ('//*[@data-stid="lodging-card-responsive"]'))
    hotels = []
    ratings_h = []
    prices = []
    total_prices = []
    specials = []
    descriptions = []
    refundables = []
    tags_h = []
    
    for WebElement in hotel_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        temp_hotel = elementSoup.find("h3", {"class": "uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start"})
        if temp_hotel is None:
            continue
        else:
            hotels.append(temp_hotel.text)

        temp_rating_h = elementSoup.find("span", {"class": "uitk-badge-base-text"})
        if temp_rating_h is None:
            ratings_h.append('NaN')
        else:
            ratings_h.append(temp_rating_h.text)

        temp_price = elementSoup.find("div", {"class": "uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme"})
        if temp_price is None:
            prices.append('NaN')
        else:
            prices.append(temp_price.text)

        temp_total = elementSoup.find("div", {"class": "uitk-text uitk-type-end uitk-type-200 uitk-type-regular uitk-text-default-theme"})
        if temp_total is None:
            total_prices.append('NaN')
        else:
            total_prices.append(temp_total.text)

        temp_special = elementSoup.find("div", {"class": "uitk-text uitk-type-200 uitk-type-bold uitk-text-default-theme"})
        if temp_special is None:
            specials.append('NaN')
        else:
            specials.append(temp_special.text)

        temp_description = elementSoup.find("div", {"class": "uitk-text uitk-type-200 uitk-text-default-theme"})
        if temp_description is None:
            descriptions.append('NaN')
        else:
            descriptions.append(temp_description.text)

        temp_refund = elementSoup.find("div", {"class": "uitk-text uitk-type-300 uitk-text-positive-theme"})
        if temp_refund is None:
            refundables.append('NaN')
        else:
            refundables.append(temp_refund.text)

        temp_tags_h = elementSoup.find_all("div", {"class": "uitk-text truncate-lines-2 uitk-type-200 uitk-text-default-theme"})
        tags_text_h = [tag.text for tag in temp_tags_h]
        tags_h.append(tags_text_h)

    driver.quit()  # Make sure to close the webdriver when done



    return jsonify({
        "hotels": [
            {
            "hotel_name": hotels[i],
            "rating": ratings_h[i],
            "price": prices[i],
            "total_price": total_prices[i],
            "special": specials[i],
            "description": descriptions[i],
            "refundable": refundables[i],
            "tags": tags_h[i]
            } for i in range(10)
        ],
        "type": "hotels"
    })

if __name__ == '__main__':
    app.run(debug=True)