import cost_class

def methodThree(movieid_low, movieid_high, actorid_low, actorid_high):
    #Create object to hold this method's cost information
    obj_1 = cost_class.CostData()
    
    # IDs of actors that match the criteria
    actor_ids = set()
    
    page_index = 1
    
    #-------------------------------------------------------------------------------------------------------------------
    # infinite loops rule!
    # we're looping through the files in the movieroles_table directory
    while 1:
        
        # try to see if a page at the current index exists
        try:
            # if the number of actors found is the max possible, break outer loop
            if actorid_low != '*' and actorid_high != '*' and len(actor_ids) == int(actorid_high) - int(actorid_low) + 1:
                break
            
            # open the file
            file = open('movieroles_table/page' + page_index + '.txt', 'r')
            
            # loop through the lines in the page
            for line in file:
                row_array = [x.strip() for x in line.split(',')]
                
                # ensure movieid and actorid match the line's ids
                if(((movieid_low == '*' and movieid_high == '*') or
                    (movieid_low == '*' and int(row_array[3]) <= int(movieid_high)) or 
                    (movieid_high == '*' and int(row_array[3]) >= int(movieid_low)) or 
                    (int(row_array[3]) >= int(movieid_low) and int(row_array[3]) <= int(movieid_high))) and 
                   
                   ((actorid_low == '*' and actorid_high == '*') or
                    (actorid_low == '*' and int(row_array[0]) <= int(actorid_high)) or 
                    (actorid_high == '*' and int(row_array[0]) >= int(actorid_low)) or 
                    (int(row_array[0]) >= int(actorid_low) and int(row_array[0]) <= int(actorid_high)))):
                        # if so, append to the set!
                        actor_ids.add(int(row_array[0]))
                        
                        # if the number of actors found is the max possible, break inner loop
                        if actorid_low != '*' and actorid_high != '*' and len(actor_ids) == int(actorid_high) - int(actorid_low) + 1:
                            break
            
            # increment index to next page
            page_index += 1
            
        # if it fails, we're done!
        except IOError as e:
            break
    
    # reset page index
    page_index = 1
    
    #-------------------------------------------------------------------------------------------------------------------
    # now, we're looping through the files in the actors_table directory
    while 1:
        try:
            # if no actors remain, break outer loop
            if len(actor_ids) == 0:
                break
            
            # open the file
            file = open('actors_table/page' + page_index + '.txt', 'r')
            
            # loop through the lines in the page
            for line in file:
                row_array = [x.strip() for x in line.split(',')]
                
                # if the actor id is one we marked as correct
                if int(row_array[1]) in actor_ids:
                    
                    # add their full name to the list of names
                    obj_1.actor_names.add(row_array[2] + " " + row_array[3])
                    
                    # remove the index to speed up searches
                    actor_ids.discard(int(row_array[1]))
                
                # if no actors remain, break inner loop
                if len(actor_ids) == 0:
                    break
            
        # if it fails, we're done!
        except IOError as e:
            break