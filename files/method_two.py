import cost_class

def methodTwo(movieid_low, movieid_high, actorid_low, actorid_high):
    #Create object to hold this method's cost information
    obj_1 = cost_class.CostData()

    #Open root file of movieroles_ma_idx
    root_data = open('movieroles_ma_idx/root.txt', 'r')

    #Add one to total cost and mr_idx_p to account for root file
    obj_1.total_cost_p += 1
    obj_1.mr_idx_p += 1

    #-------------------------------------------------------------------------------------------------------------------
    #Loop through lines in root.txt of movieroles_ma_idx, find proper internal leaf file

    row_num = 0
    for line in root_data:
        row_num += 1

        if line.strip() == '':
            continue

        if line.strip() == "internal":
            continue

        root_array = [x.strip() for x in line.split(',')]

        #Case to handle when there is no minimum movieid set (just pick first internal node)
        if movieid_low == '*' and row_num == 2:
            internal_location = "movieroles_ma_idx/" + root_array[2]
            internal_data = open(internal_location, 'r')
            internal_data.seek(0)

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1
            break
        
        #Find internal node that contains minimum movieid
        if int(movieid_low) <= int(root_array[0]):
            internal_location = "movieroles_ma_idx/" + root_array[2].strip()
            internal_data = open(internal_location, 'r')
            internal_data.seek(0)

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1
            break


    #-------------------------------------------------------------------------------------------------------------------
    #Loop through lines in internal file, find leaf node that contains minimum movieid
    row_num = 0
    for line_one in internal_data:
        row_num += 1
        if line_one.strip() == "internal":
            continue

        internal_array = [x.strip() for x in line_one.split(',')]

        #Case to handle where there is no minimum movieid set (just pick first internal node)
        if movieid_low == '*' and row_num == 2:
            leaf_location = "movieroles_ma_idx/" + internal_array[2].strip()
            leaf_data = open(leaf_location, 'r')
            leaf_data.seek(0)

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1

            break
        
        #Find leaf that contains the minimum movieid of the query
        if int(movieid_low) <= int(internal_array[0]):
            leaf_location = "movieroles_ma_idx/" + internal_array[2].strip()
            leaf_data = open(leaf_location, 'r')
            leaf_data.seek(0)

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1
            
            break
    #-------------------------------------------------------------------------------------------------------------------
    #Loop through lines in leaf file(s), add matching actorids to a set
    actorid_set = set()
    leaf_location_b = leaf_location
    should_break = False
    
    while (True): 
        #Set file to read through
        leaf_data.close()
        leaf_data = open(leaf_location_b, 'r')
        
        for line_two in leaf_data:
    
            if line_two.strip() == '':
                should_break = True
                break
    
            if line_two.strip() == "leaf":
                continue
    
            #Reached end of file, go to next leaf file listed
            if (line_two.strip())[0] == 'l' and line_two.strip() != "leaf":
                leaf_location_b = "movieroles_ma_idx/" + line_two.strip()
    
                obj_1.total_cost_p += 1
                obj_1.mr_idx_p += 1
    
                break
    
            leaf_array = [x.strip() for x in line_two.split(',')]
    
            #Stop searching through leaf when movieid > movieid_high
            if movieid_high != '*' and (int(leaf_array[0]) > int(movieid_high)):
                should_break = True
                break
    
            #If actorid is in specified range, add actorid to actorid_set
            if (actorid_low == '*' or (int(leaf_array[1]) >= int(actorid_low))) and (actorid_high == '*' or (int(leaf_array[1]) <= int(actorid_high))) and (movieid_low == '*' or (int(leaf_array[0]) >= int(movieid_low))) and (movieid_high == '*' or (int(leaf_array[0]) <= int(movieid_high))):
                actorid_set.add(leaf_array[1].strip())
            
        if should_break == True:
            break
    #-------------------------------------------------------------------------------------------------------------------
    #Loop through actor table files, add matching actor names to return set
    
    leaf_location_c = "actors_table/page1.txt"
    leaf_data_c = open(leaf_location_c,'r')
    should_break_c = False
    file_num = 1
    
    while (True): 
        if file_num != 2105:
            #Set file to read through
            leaf_data_c.close()
            leaf_location_c = "actors_table/page" + str(file_num) + ".txt"
            leaf_data_c = open(leaf_location_c, 'r')
            
            obj_1.total_cost_p += 1
            obj_1.a_tab_p += 1
        else:
            break
        
        #Go through each line of actor table file
        for line_three in leaf_data_c:
            actor_array = [x.strip() for x in line_three.split(',')]
            
            if actor_array[1] in actorid_set:
                if len(actor_array) == 3:
                    name = actor_array[2]
                else:
                    name = actor_array[2] + " " + actor_array[3]
                    
                obj_1.actor_names.add(name)
                actorid_set.discard(actor_array[1])
                
                if len(actorid_set) == 0:
                    should_break_c = True
                    break
                
        file_num += 1
        if should_break_c == True:
            break
    
    return obj_1
    