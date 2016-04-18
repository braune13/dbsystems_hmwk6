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
            
            print "No minimum movieid, picking first internal node: " + internal_location

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
            
            print "No minimum movieid, picking first internal node: " + leaf_location

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
        #leaf_data.seek(0) 
        
        for line_two in leaf_data:
    
            if line_two.strip() == '':
                should_break = True
                continue
    
            if line_two.strip() == "leaf":
                continue
    
            #Reached end of file, go to next leaf file listed --- WHERE IT FUCKS UP
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
                actorid_set.add(leaf_array[1])
            
        if should_break == True:
            break
    print "NUMBER OF ACTOR_ID'S FOUND: " + str(len(actorid_set))
    #-------------------------------------------------------------------------------------------------------------------
    return obj_1
    