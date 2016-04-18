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
            # open the file
            file = open('movieroles_table/page' + str(page_index) + '.txt', 'r')
            
            # loop through the lines in the page
            for line in file:
                row_array = [x.strip() for x in line.split(',')]
                
                # -----------------------
                # If the name had a comma, we need to readjust
                if len(row_array) > 5 and not row_array[3].isdigit():
                    # print row_array
                    adjusted_array = []
                    adjusted_array.append(row_array[0])
                    adjusted_array.append(row_array[1])
                    adjusted_array.append(row_array[2] + ', ' + row_array[3])
                    adjusted_array.append(row_array[4])
                    adjusted_array.append(row_array[5])
                    row_array = adjusted_array
                # -----------------------
                
                # ensure movieid and actorid match the line's ids
                if(((movieid_low == '*' and movieid_high == '*') or
                    (movieid_low == '*' and movieid_high != '*' and int(row_array[3]) <= int(movieid_high)) or 
                    (movieid_high == '*' and movieid_low != '*' and int(row_array[3]) >= int(movieid_low)) or 
                    (movieid_high != '*' and movieid_low != '*' and int(row_array[3]) >= int(movieid_low) and int(row_array[3]) <= int(movieid_high))) and
                   
                   ((actorid_low == '*' and actorid_high == '*') or
                    (actorid_low == '*' and actorid_high != '*' and int(row_array[0]) <= int(actorid_high)) or 
                    (actorid_high == '*' and actorid_low != '*' and int(row_array[0]) >= int(actorid_low)) or 
                    (actorid_high != '*' and actorid_low != '*' and int(row_array[0]) >= int(actorid_low) and int(row_array[0]) <= int(actorid_high)))):
                        # if so, append to the set!
                        actor_ids.add(int(row_array[0]))
            
            # increment index to next page
            page_index += 1
            
        # if it fails, we're done!
        except IOError as e:
            break
    
    # log the total number of pages traversed
    obj_1.mr_tab_p = page_index - 1
    
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
            file = open('actors_table/page' + str(page_index) + '.txt', 'r')
            
            # print page_index
            
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
                
            # increment index to next page
            page_index += 1
            
        # if it fails, we're done!
        except IOError as e:
            break
        
    # log the total number of pages traversed
    obj_1.a_tab_p = page_index - 1
    
    # combine page counts for overall ttoal
    obj_1.total_cost_p = obj_1.mr_tab_p + obj_1.a_tab_p
    
    return obj_1