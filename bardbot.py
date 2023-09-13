from bardapi import BardCookies

cookie_dict = {
    "__Secure-1PSID": "aQgNOlozJyAYWkoC9wWToeRz3vo2De_qhY4NoQVVKZ1OXqYOTc3BNIh1uFTEBm9geGDwjQ.",
    "__Secure-1PSIDTS": "sidts-CjIBSAxbGQ_9x3QO_lx7y--gdUwHWPscWc89hyZ2fwYaa7jYExRyVOnjCwvGX6r6bsCD6xAA",
    # Any cookie values you want to pass session object.
}
bard = BardCookies(cookie_dict=cookie_dict)

def get_user_input(prompt):
    return input(prompt + " ")

destination = get_user_input("Where would you like to go?")
departure_date = get_user_input("When are you planning to depart?")
return_date = get_user_input("When are you planning to return?")
budget = get_user_input("What is your budget range?")
accommodation = get_user_input("What are some of your interests?")
activities = get_user_input("Where would you like to stay?")
people = get_user_input("Who and how many people are you staying with?")
people = get_user_input("Who and how many people are you staying with?")









print(bard.get_answer("hello")['content'])
