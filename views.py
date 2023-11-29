from flask import Blueprint, render_template, request, jsonify
import openai

# Defining the classes for each feature and ways to access them
class DailyPlanner(Chatbot):
    def __init__(self):
        self.dailyPlan = ""

    def setDailyPlan(self, newDailyPlan):
        self.dailyPlan = newDailyPlan
    

class PackingList(Chatbot):
    def __init__(self):
        self.packList = ""

    def setPackList(self, newPackList):
        self.packList = newPackList


class Hotel(Chatbot):
    def __init__(self):
        self.hotelList = ""

    def setHotelList(self, newHotelList):
        self.hotelList = newHotelList


class Restaurant(Chatbot):
    def __init__(self):
        self.restaurantList = ""

    def setRestaurantList(self, newRestaurantList):
        self.restaurantList = newRestaurantList


class Budget(Chatbot):
    def __init__(self):
        self.budgetList = ""

    def setBudget(self, newBudgetList):
        self.budgetList = newBudgetList


# Defining the chabotbot class and its message collecting system
class Chatbot:
    def __init__(self, model_name, client):
        self.model_name = model_name
        self.client = client


    def chat_with_openai(self, prompt):
        # Add user's message to the list of messages
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        # Add the current user's message
        messages.append({'role': 'user', 'content': prompt})
        # Get a response from OpenAI
        response = self.client.chat.completions.create(model=self.model_name,
        messages=messages)

        chatbot_response = response.choices[0].message['content']
        
        return chatbot_response.strip()
    
    def factory(self):
        # Object Declarations
        dailyPlanner_1 = DailyPlanner()
        packingList_1 = PackingList()
        hotel_1 = Hotel()
        restaurant_1 = Restaurant()
        budget_1 = Budget()

        return dailyPlanner_1, packingList_1, hotel_1, restaurant_1, budget_1


views = Blueprint(__name__, "views")

# Renders index.html as the template
@views.route("/")
def home():
    return render_template("index.html")