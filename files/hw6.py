#Created by Erica Braunschweig (braune)

import sys

#Global list to hold queries and their parameters (will be a list of lists)
queries_params = []

#===============================================================================
#CostData class to hold cost information for each method run

class CostData:
    def __init__(self):
        self.total_cost_p = 0
        self.mr_idx_p = 0
        self.mr_tab_p = 0
        self.a_idx_p = 0
        self.a_tab_p = 0
    
#====================================================================================
#Function to read through input file and parse search parameters into a dict of lists

def parseInputData():
    
    
    #Get input file name from command line and open it as read only
    input_file = sys.argv[1]
    input_data = open(input_file, 'r')
    
    for line in input_data:
        #For line of input, split on ',' and get rid of any whitespace
        query_params = [x.strip() for x in line.split(',')]
        
        #Put this list of query parameters into the list of all query parameters
        queries_params.append(query_params)

        
    print queries_params
    
    return queries_params
#==================================================================================== 

#First scan the movieroles_ma_idx index to find all actors, then actors_id_idx to find
#the names of these actors and print
def methodOne():
    #Create object to hold this method's cost information
    obj_1 = CostData()

    
#====================================================================================

#For each query, call each of the three search methods
def runQuery():
    #---------------------------------------------------------------------------
    #Print out what the query is, result header
    for params in queries_params:
        output = "Query: "
        
        for item in params:
            output += item + ','
            
        output = output[:-1]
        print output
        
        #Print out "Result:" and an extra newline
        print "Result:\n"
    #---------------------------------------------------------------------------
    methodOne()
    
#===================================================================================
#Main
parseInputData()
runQuery()