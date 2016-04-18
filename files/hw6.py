#Created by Erica Braunschweig (braune) and Justin Etzine (etzinj)

import sys
import method_one
import method_two
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
    #Print out what the query is, result header
    for params in queries_params:
        output = "Query: "
        
        for item in params:
            output += item + ','
            
        output = output[:-1]
        print output

        #Run all three methods
        method_1_obj = method_one.methodOne(params[0], params[1], params[2], params[3])
        method_2_obj = method_two.methodTwo(params[0], params[1], params[2], params[3])
        method_3_obj = method_three.methodThree(params[0], params[1], params[2], params[3])
    
        print ""
        
        #Print out actor names that query returned
        output_string = "Results (" + str(len(method_1_obj.actor_names)) + " total):"
        print output_string
        for name in method_1_obj.actor_names:
            print "\t" + name
        
        print ""
        
        print "Method 1 total cost: " + str(method_1_obj.total_cost_p) + " pages"
        print "\t" + str(method_1_obj.mr_idx_p) + " page movieroles_ma_idx index"
        print "\t" + str(method_1_obj.a_idx_p) + " page actors_id_idx index"
        print "\t" + str(method_1_obj.a_tab_p) + " page actors_table\n"

        print "Method 2 total cost: " + str(method_2_obj.total_cost_p) + " pages"
        print "\t" + str(method_2_obj.mr_idx_p) + " page movieroles_ma_idx index"
        print "\t" + str(method_2_obj.a_tab_p) + " page actors_table\n"
        
        print "Method 3 total cost: " + str(method_3_obj.total_cost_p) + " pages"
        print "\t" + str(method_3_obj.mr_tab_p) + " page movieroles_table"
        print "\t" + str(method_3_obj.a_tab_p) + " page actors_table\n"
        
#=======================================================================================================================
#Main
parseInputData()
runQuery()