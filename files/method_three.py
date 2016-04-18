import cost_class

def methodThree(movieid_low, movieid_high, actorid_low, actorid_high):
    #Create object to hold this method's cost information
    obj_1 = cost_class.CostData()
    
    page_index = 1
    
    while(true):
        file = open('movieroles_table/page' + page_index + '.txt', 'r')
        
        for line in file:
            row_array = [x.strip() for x in line.split(',')]
            
            if(int(row_array[0]))