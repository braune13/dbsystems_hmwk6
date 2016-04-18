#Created by Erica Braunschweig (braune)

import sys
import method_one_backup
import method_three
import cost_class

#Global list to hold queries and their parameters (will be a list of lists)
queries_params = []

#=======================================================================================================================
#Function to read through input file and parse search parameters into a list of lists

def parseInputData():
    
    
    #Get input file name from command line and open it as read only
    input_file = sys.argv[1]
    input_data = open(input_file, 'r')
    
    for line in input_data:
        #For line of input, split on ',' and get rid of any whitespace
        query_params = [x.strip() for x in line.split(',')]
        
        #Put this list of query parameters into the list of all query parameters
        queries_params.append(query_params)
        
#=======================================================================================================================

#For each query, call each of the three search methods

def runQuery():
    #-------------------------------------------------------------------------------------------------------------------
    #Print out what the query is, result header
    for params in queries_params:
        output = "Query: "
        
        for item in params:
            output += item + ','
            
        output = output[:-1]
        print output

        #Run all three methods
        method_1_obj = method_one_backup.methodOne(params[0], params[1], params[2], params[3])

        #Print out actor names that query returned
        output_string = "Results: (" + str(len(method_1_obj.actor_names)) + " total):"
        print output_string
        for name in method_1_obj.actor_names:
            print "\t" + name

        #Print Method One cost details
        print "Method One total cost: " + str(method_1_obj.total_cost_p) + " pages"
        print str(method_1_obj.mr_idx_p) + " page movieroles_ma_idx index"
        print str(method_1_obj.a_idx_p) + " page actors_id_idx index"
        print str(method_1_obj.a_tab_p) + " page actors_table"


        print "\n\n\n"
#=======================================================================================================================
#Main
parseInputData()
runQuery()