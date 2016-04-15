import sys
#====================================================================================
#Function to read through input file and parse search parameters into a dict of lists
def parseInputData():
    
    queries_params = {}
    
    #Get input file name from command line and open it as read only
    input_file = sys.argv[1]
    input_data = open(input_file, 'r')
    index = 0
    
    for line in input_data:
        #For line of input, split on ',' and get rid of any whitespace
        query_params = [x.strip() for x in line.split(',')]
        
        #Put this list of query parameters into the dictionary of all query parameters
        queries_params[index] = query_params
        
        index += 1
        
    print queries_params
    
    return queries_params
#==================================================================================== 
#First scan the movieroles_ma_idx index to find all actors, then actors_id_idx to find
#the names of these actors and print
def methodOne():
    
#====================================================================================
#Main
parseInputData()