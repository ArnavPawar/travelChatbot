from bardapi import BardCookies

cookie_dict = {
    "__Secure-1PSID": "aQgNOlozJyAYWkoC9wWToeRz3vo2De_qhY4NoQVVKZ1OXqYOTc3BNIh1uFTEBm9geGDwjQ.",
    "__Secure-1PSIDTS": "sidts-CjIBSAxbGfMRLt5hEB833rhgyRhN5T9IS4qiJgIrCRY5Linwuk6mgKD5JOS0UiAMDFKR4xAA",
    # Any cookie values you want to pass session object.
}

def get_user_input(prompt):
    return input(prompt + " ")

#destination = get_user_input("Where would you like to go?")
destination = ("Where would you like to go?"+"Long island")

#city = get_user_input("What city and/or adress are you planning on staying?")
city = ("What city and/or adress are you planning on staying?"+"dix hills")

#departure_date = get_user_input("What time of month are you going?")
departure_date = ("What time of month are you going?"+"july 21st")

#return_date = get_user_input("How long are you planning on staying?")
return_date = ("How long are you planning on staying?"+"5 days")

#budget = get_user_input("What is your budget range?")
budget = ("What is your budget range?"+"2000$")

#accommodation = get_user_input("What are some of your interests?")
accommodation = ("What are some of your interests?"+"I like swimming, biking, sports like basketball and soccer, food, seafood, the beach, painting, and going out and going to concerts")

#activities = get_user_input("Where would you like to stay?")
activities = ("Where would you like to stay?"+"dix hills area in an airbnb")

#people = get_user_input("Who and how many people are you staying with?")
people = ("Who and how many people are you staying with?"+"4 people")

#planned = get_user_input("What do you have planned already?")
planned = ("What do you have planned already?"+"nothing yet")

#otherInfo = get_user_input("Add any other info that you think is important for the trip?")
otherInfo = ("Add any other info that you think is important for the trip?"+"we are college students that want to have a fun vacation")


bard = BardCookies(cookie_dict=cookie_dict)
print(("Can you plan a trip based on all of these questions and answers:"+destination+city+departure_date+return_date+budget+accommodation+activities+activities+people+planned+otherInfo+ "Also can you plan this trip in this order: ONLY 1 Daily schedule with links for each activity and an estimated price for the activity for everyone(do not provide more than 1 itinerary on the output), ONE A packing list, after providing a daily activiy and packing list provide 10 hotel or airbnb reccomendation for the whole trip with links and lastly 10 reccomended reasturant locations for the whole trip based on the given information and location"))
