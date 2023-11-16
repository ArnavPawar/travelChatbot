input_string = """Daily Planner:
Day 1:
- Visit the Millennium Park to see iconic attractions like the Cloud Gate sculpture (Free)
- Enjoy a soccer match at the Soldier Field Stadium ($50 per person)
- Explore the Art Institute of Chicago ($25 per person)
- Dinner at Giordano's for some delicious deep-dish pizza ($20 per person)

Day 2:
- Take a guided architectural river cruise to admire the beautiful skyline ($40 per person)
- Visit the Field Museum to learn about natural history ($25 per person)
- Watch a Chicago Fire soccer game at Toyota Park ($30 per person)
- Dinner at Portillo's for Chicago-style hot dogs and Italian beef sandwiches ($15 per person)

Day 3:
- Take a stroll along Navy Pier and enjoy the Ferris wheel ride ($20 per person)
- Explore the Shedd Aquarium and see amazing underwater creatures ($40 per person)
- Attend a soccer training session with Chicago Fire Academy ($30 per person)
- Dinner at Lou Malnati's for another taste of deep-dish pizza ($20 per person)

Day 4:
- Visit the Chicago Sports Museum to learn about the city's sports history ($15 per person)
- Watch a soccer game at Wrigley Field with Chicago Red Stars ($40 per person)
- Take a walk along the Magnificent Mile for shopping and sightseeing (Free)
- Dinner at Girl & The Goat for a unique dining experience ($50 per person)

Day 5:
- Explore the Museum of Science and Industry ($30 per person)
- Join a soccer skills workshop at the Chicago KICS Soccer Academy ($20 per person)
- Watch a soccer game at SeatGeek Stadium with Chicago House AC ($30 per person)
- Dinner at Alinea for a Michelin-starred fine dining experience ($200 per person)

Day 6:
- Visit the Buckingham Fountain and enjoy its beautiful water display (Free)
- Explore the Chicago History Museum to learn about the city's past ($20 per person)
- Attend a soccer match with Chicago Lions Rugby Club ($20 per person)
- Dinner at The Girl & The Goat for another delicious meal ($50 per person)

Day 7:
- Relax and enjoy a day at Grant Park (Free)
- Explore the Museum of Contemporary Art ($15 per person)
- Watch a soccer game at CIBC Fire Pitch with FC Chicago ($25 per person)
- Dinner at Swift & Sons for a steakhouse experience ($100 per person)

Packing List:
- Warm winter clothing (coats, sweaters, hats, gloves)
- Comfortable walking shoes
- Soccer gear (cleats, balls, jerseys)
- Daypack for carrying essentials
- Camera or smartphone for capturing memories
- Electrical adapters for charging devices
- Travel-sized toiletries
- Cash and/or credit cards
- Travel insurance documents

Restaurant Recommendations:
1. Giordano's: https://giordanos.com/
2. Portillo's: https://www.portillos.com/
3. Lou Malnati's: https://www.loumalnatis.com/
4. Girl & The Goat: https://www.girlandthegoat.com/
5. Alinea: https://www.alinearestaurant.com/
6. The Girl & The Goat: https://www.girlandthegoat.com/
7. Swift & Sons: https://www.swiftandsonschicago.com/
8. The Purple Pig: https://thepurplepigchicago.com/
9. The Gage: https://www.thegagechicago.com/
10. The Publican: https://www.publicananker.com/

Hotel Recommendations:
1. The Langham, Chicago: https://www.langhamhotels.com/en/the-langham/chicago/
2. The Peninsula Chicago: https://www.peninsula.com/en/chicago/5-star-luxury-hotel-michigan-avenue
3. The Ritz-Carlton, Chicago: https://www.ritzcarlton.com/en/hotels/chicago
4. The JW Marriott Chicago: https://www.marriott.com/hotels/travel/chijw-jw-marriott-chicago/
5. The LondonHouse Chicago: https://londonhousechicago.com/
6. Kimpton Hotel Allegro: https://www.allegrochicago.com/
7. The Gwen, a Luxury Collection Hotel, Chicago: https://www.thegwenchicago.com/
8. The Godfrey Hotel Chicago: https://www.godfreyhotelchicago.com/
9. Radisson Blu Aqua Hotel Chicago: https://www.radissonhotels.com/en-us/hotels/radisson-blu-chicago
10. The James Chicago - Magnificent Mile: https://www.jameshotels.com/chicago

Budget Breakdown:
- Total estimated cost for daily activities: $1,045 per person
- Total estimated cost for meals: $295 per person (approximately $42 per day)
- Hotel/ Airbnb costs may vary depending on the chosen option. It is recommended to check the provided links for pricing and availability.
- Keep in mind additional expenses like transportation, souvenirs, and any unplanned activities.
"""

sections = input_string.split('\n\n')
# print(sections)
DailyPlanner = ""
PackList = ""
Restrant = ""
Hotel = ""
Budget = ""

for sec in sections:
    if sec.startswith("Daily Planner:") or sec.startswith("Day"):
        DailyPlanner+=sec+"\n"
    elif sec.startswith("Packing List:"):
        PackList+=sec
    elif sec.startswith("Restaurant Recommendations:"):
        Restrant+=sec
    elif sec.startswith("Hotel Recommendations:"):
        Hotel+=sec
    elif sec.startswith("Budget Breakdown:"):
        Budget+=sec
    else:
        print("NOT ENOUGH INFORAMTION")
# print(sections

print(DailyPlanner)
print(PackList)
print(Restrant)
print(Hotel)
print(Budget)

# for sec in sections:
#     if sec == "Daily Planner":
    
#     if sec == ""

# Create a dictionary to store each section with its heading
