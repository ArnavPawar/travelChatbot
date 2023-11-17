from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI

#Defining the chabotbot class and its message collecting system
class Chatbot:
    def __init__(self, model_name, client):
        self.model_name = model_name
        self.client = client

    def chat_with_openai(self, prompt):
        #Add user's message to the list of messages
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        #Add the current user's message
        messages.append({'role': 'user', 'content': prompt})
        #Get a response from OpenAI
        response = self.client.chat.completions.create(model=self.model_name,
        messages=messages)

        chatbot_response = response.choices[0].message.content
        
        return chatbot_response.strip()

#Defining the classes for each feature and ways to access them
class DailyPlanner:
    def __init__(self):
        self.dailyPlan = ""

    def setDailyPlan(self, newDailyPlan):
        self.dailyPlan = newDailyPlan
    
class PackingList:
    def __init__(self):
        self.packList = ""

    def setPackList(self, newPackList):
        self.packList = newPackList

class Hotel:
    def __init__(self):
        self.hotelList = ""

    def setHotelList(self, newHotelList):
        self.hotelList = newHotelList

class Restaurant:
    def __init__(self):
        self.resturantList = ""

    def setRestaurantList(self, newRestaurantList):
        self.restaurantList = newRestaurantList

class Budget:
    def __init__(self):
        self.budgetList = ""

    def setBudget(self, newBudgetList):
        self.budgetList = newBudgetList



views = Blueprint(__name__, "views")

#Renders index.html as the template
@views.route("/")
def home():
    return render_template("index.html")

#Extracts text prompts
@views.route("/", methods=["GET","POST"])
def handle_post_request():

    #Get JSON data from the request
    data = request.get_json()
    #Extract 'text_prompt' from the JSON data
    text_prompt = data.get('text_prompt')  

    #Print received data to the terminal
    print("Received data:", text_prompt) 

    #Creates chatbot object
    client = OpenAI(api_key="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")
    model_name = "gpt-3.5-turbo"
    chatbot_1 = Chatbot(model_name, client)

    tripPlan=chatbot_1.chat_with_openai(text_prompt)

    sections = tripPlan.split('\n\n')
    
    #Object Declarations
    dailyPlanner_1 = DailyPlanner()
    packingList_1 = PackingList()
    hotel_1 = Hotel()
    restaurant_1 = Restaurant()
    budget_1 = Budget()

    #Everytime a new portion for each section is created
    #It is added to it's respective object
    for sec in sections:
        if sec.startswith("Daily Planner:") or sec.startswith("Day"):
            newPlan = dailyPlanner_1.dailyPlan + sec + "\n"
            dailyPlanner_1.setDailyPlan(newPlan)
            print("PLAN:::"+dailyPlanner_1.dailyPlan)
        elif sec.startswith("Packing List"):
            newPackList = packingList_1.packList + sec + "\n"
            packingList_1.setPackList(newPackList)
            print("PACK:::"+packingList_1.packList)
        elif sec.startswith("Restaurant Recommendations"):
            newRestaurantList = restaurant_1.resturantList + sec + "\n"
            restaurant_1.setRestaurantList(newRestaurantList)
            print("RES:::"+restaurant_1.restaurantList)
        elif sec.startswith("Hotel Recommendations"):
            newHotelList = hotel_1.hotelList + sec + "\n"
            hotel_1.setHotelList(newHotelList)
            print("HOTEL:::"+hotel_1.hotelList)   
        elif sec.startswith("Budget Breakdown"):
            newBudgetList = budget_1.budgetList + sec + "\n"
            budget_1.setBudget(newBudgetList)
            print("BUG:::"+budget_1.budgetList)
        else:
            print("NOT ENOUGH INFORAMTION")

    return jsonify({
        "response": "Received data: " + text_prompt,
        "trip": tripPlan,
        "DailyPlanne": dailyPlanner_1.dailyPlan,
        "PackList": packingList_1.packList,
        "Restrant": restaurant_1.restaurantList,
        "Hotel": hotel_1.hotelList,
        "Budget": budget_1.budgetList
        })