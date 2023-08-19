import pandas as pd

#import csv files
flightsData=pd.read_csv("flights.csv")
hotelsData=pd.read_csv("hotels.csv")
usersData=pd.read_csv("users.csv")



#choose the spacific coloums 

sp_users=usersData[["code", "name"]]
sp_hotels=hotelsData[["userCode","name" , "place" , "price"]]
sp_flights=flightsData[["userCode",'from','to','flightType','price']]


#sorted_hotels = filterd_hotels.sort_values(by=["userCode", "price"])
#sorted_flights = filterd_flights.sort_values(by=["userCode", "price"])


#sorted_hotels_list = sorted_hotels.values.tolist()
#sorted_flights_list = sorted_flights.values.tolist()


# Remove duplicate rows
filtered_hotels = sp_hotels.drop_duplicates()
filtered_flights = sp_flights.drop_duplicates()


def recommendtion (user_name , budget , num , location):
    #choose the spacific user you enter
    spacific_user = sp_users.loc[sp_users['code'] == user_name]

    #choose spacific flights from the user loaction
    spacific_flights=filtered_flights.loc[filtered_flights['from'] == location]

    # Calculate average prices for flights to each destination, considering both outgoing and return trips
    average_flight_prices = spacific_flights.groupby('to')['price'].mean().reset_index()

    # Sort flights dataset by average price
    sorted_flights = average_flight_prices.sort_values('price')

    #now it's the start of my algorithm

    # Select unique cities based on the lowest average flight prices
    selected_cities = sorted_flights['to'].tolist()[:num]

    #make the dp table(2d with (num_cities + 1) row and (budget + 1) coloum (all intilize to be 0)
    dp_table = [[0] * (budget + 1) for _ in range(num + 1)]

    #dp table to calc the total budget
    budget_table = [[0] * (budget + 1) for _ in range(num + 1)]

    # Iterate over each city in ( selected city )and budget combination
    for i in range (0,num+1):
        city=selected_cities[i-1]
        city_flight_prices = spacific_flights.loc[spacific_flights['to'] == city]['price']
        city_flight_price = int(city_flight_prices.mean())

        city_hotels = filtered_hotels.loc[filtered_hotels['place'] == city]
        hotel_prices = city_hotels['price']
        average_hotel_price = int(hotel_prices.mean())

        for j in range(1, budget + 1):

            max_cities_without_current = dp_table[i - 1][j]
            '''
                      Retrieves the maximum number of cities that can be visited without considering the current city and budget.
                      dp_table[i - 1][j] accesses the corresponding cell in the previous row of the dynamic programming table.
            '''

            #initializes the maximum number of cities that can be visited considering the current city and budget.
            #This value will be updated in the next loop based on hotel prices.
            max_cities_with_current = 0

            for hotel_price in hotel_prices:

                # Checks if the total cost of the flight and the current hotel price is less than or equal to the current budget (j).
                # If the condition is satisfied, it means the current city can be visited within the budget.
                if city_flight_price + int(hotel_price) <= j:
                    #Updates the maximum number of cities that can be visited considering the current city and budget.
                    #It compares the current value of max_cities_with_current with the number of cities that can be visited with the remaining budget after considering the current city and hotel.
                    #dp_table[i - 1][j - city_flight_price - int(hotel_price)] retrieves the corresponding cell in the previous row and the remaining budget.
                    #it's the knapsacking idea with using the dp
                    max_cities_with_current = max(max_cities_with_current, dp_table[i - 1][j - city_flight_price - int(hotel_price)] + 1)
            #Updates the current cell in the dynamic programming table with the maximum value of cities that can be visited.
            #It takes the maximum between max_cities_without_current (the number of cities without considering the current city) and max_cities_with_current (the number of cities considering the current city).
            #The result is stored in dp_table[i][j].
            dp_table[i][j] = max(max_cities_without_current, max_cities_with_current)

            # Update the budget table with the total budget for each city
            if max_cities_with_current > max_cities_without_current:

                budget_table[i][j] = budget_table[i - 1][j - city_flight_price - int(hotel_price)] + city_flight_price + int(hotel_price)
            else:
                budget_table[i][j] = budget_table[i - 1][j]




    # Backtrack to find the selected cities and total budget
    recommended_cities = []

    total_budget = budget
    for i in range(num, 0, -1):
        city = selected_cities[i - 1]
        city_flight_prices = filtered_flights.loc[filtered_flights['to'] == city]['price']
        city_flight_price = int(city_flight_prices.mean())
        city_hotels = filtered_hotels.loc[filtered_hotels['place'] == city]
        hotel_prices = city_hotels['price']

        # Calculate average price for hotels in the city
        average_hotel_price = int(hotel_prices.mean())

        #These lines initialize variables used for tracking the maximum number of cities that can be visited without and with the current city, as well as the price of the selected hotel.
        max_cities_without_current = dp_table[i - 1][total_budget]
        max_cities_with_current = 0
        selected_hotel_price = 0
        '''
        This loop iterates over the hotel_prices list for the current city.
         It checks if the sum of the flight price and the current hotel price is less than or equal to the remaining budget (total_budget). 
         It also verifies if the number of cities that can be visited without the current city plus one is equal to the number of cities that can be visited with the current city, as stored in the dp_table.
        If these conditions are met, it updates max_cities_with_current and selected_hotel_price accordingly.
         Additionally, if the number of cities that can be visited with the current city is greater than the number of cities that can be visited without the current city, 
         it adds the current city and selected hotel price to the recommended_cities list, 
         adjusts the total_budget by subtracting the flight and hotel prices, and then breaks out of the loop.
        '''
        for hotel_price in hotel_prices:
            if city_flight_price + int(hotel_price) <= total_budget and dp_table[i - 1][total_budget - city_flight_price - int(hotel_price)] + 1 == dp_table[i][total_budget]:
                max_cities_with_current = dp_table[i - 1][total_budget - city_flight_price - int(hotel_price)] + 1
                selected_hotel_price = int(hotel_price)
                if max_cities_with_current > max_cities_without_current:
                    recommended_cities.append((city, selected_hotel_price))
                    total_budget -= city_flight_price + selected_hotel_price
                    break

    recommended_cities.reverse()  # Reverse the list to maintain the original order of selected cities

    return recommended_cities, total_budget


user_name =input("Enter The User Name : ")
budget = int(input("Enter Your Budget : "))
num = int(input("Enter Number of Cities You Want To Visit : "))
location = input("Enter Your Location : ")
print("Waiting...............")

recommended_cities, total_budget = recommendtion(user_name, budget, num, location)
print("Recommended cities and hotel prices:", recommended_cities)
print("Total budget:", total_budget)


'''
i build this project for the spacific users and locations in the datasets

so if you enter your name or place that not found in the datasets, error will be occured
'''































