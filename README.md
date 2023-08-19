# Travel_Recommedation_Project
Planning a Worldwide trip to a user with a recommendation system based on his budget and his last visits 


## Aim
Suppose you are planning a Worldwide trip to a user, and you have a list of N cities
he wants to visit, each with a set of attractions he would like to see. He has a fixed
budget B, and he wants to plan a trip that maximizes the number of attractions he
can visit while staying within his budget.
The problem can be solved using dynamic programming, where the state of the
problem is defined by the remaining budget and the subset of attractions that have
not yet been visited. The value of the state can be defined as the maximum number
of attractions that can be visited from that state.

Use the travel dataset which has three files’ users, flights, and hotels to build a
recommendation system.
Input: User, Budget, and Number of cities to be visited.
Output: List of recommended cities.

The provided code implements a recommendation algorithm that suggests cities and hotel prices based on user input. Let's break down the code and analyze the time complexity and techniques used in each section:
  1. Importing libraries and reading CSV files:
     *Time Complexity: O(n), where n is the total number of entries in all three CSV files. Reading CSV files has a linear time complexity based on the number of        entries.
  2. Selecting specific columns:
     *Time Complexity: O(1). Selecting specific columns from a DataFrame is a constant time operation as it does not depend on the size of thedata framee.
  3. Removing duplicate rows:
     *Time Complexity: O(m), where m is the number of rows in the DataFrame. Removing duplicates requires comparing each row to all other rows to identify          
     duplicates, which takes linear time complexity.
  4. Defining the recommendation function:
     *Time Complexity: O(numCities * budget * h), where numCities is the number of cities, budget is the user's budget, and h is the average number of hotels per   
      city. The function utilizes dynamic programming to solve the problem. It iterates over each city and budget combination, and for each combination, it checks        the hotels' prices in the specific city.
  5. Backtracking to find recommended cities:
     * Time Complexity: O(numCities * budget * h), where numCities is the number of cities, budget is the user's budget, and h is the average number of hotels per         city. The backtracking process involves iterating over each city and budget combination to find the recommended cities and remaining budget.
  6. Taking user input and displaying recommendations:
    * Time Complexity: O(1). The time complexity of taking user input and displaying recommendations is considered constant time, as it does not depend on the size       of the input or the number of recommendations.
In terms of techniques used, the code implements the following:
●Data Manipulation: The code uses the pandas library to read, filter, select columns, and remove duplicates from the CSV data. Pandas provides powerful tools for data manipulation and analysis.
●Dynamic Programming: The recommendation function utilizes dynamic programming to solve the problem efficiently. It builds a dynamic programming table to store the maximum number of cities visited for each budget and uses this table for backtracking to find the recommended cities and remaining budget.
Overall, the time complexity of the code is mainly determined by the size of the input data (number of entries in CSV files) and the number of cities, budget, and hotels. The use of dynamic programming allows for efficient computation of the recommendations within the given constraints.
