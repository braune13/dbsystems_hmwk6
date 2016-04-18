# dbsystems_hmwk6
Database Systems Homework Six
Created by: Erica Braunschweig (braune) and Justin Etzine (etzinj)

To run program put the following in the command line:
python hw6.py name_of_input_file.txt

File Breakdown:
hw6.py - main file that takes in input file, parses it, runs each method, and prints the resulting data
cost_class.py - class that holds all method cost data and an array of actors that met the query parameters
method_one.py - runs method one function and returns result in CostClass object
method_two.py - runs method two function and returns result in CostClass object
method_three.py - runs method three function and returns result in CostClass object

Known Issues:
Program may not parse file lines with extra commas properly.  We mitigated the issue as best as we could,
but we may not have caught a comma related issues.