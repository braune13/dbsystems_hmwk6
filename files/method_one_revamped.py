import cost_class

def methodOne(movieid_low, movieid_high, actorid_low, actorid_high):
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
    #All actorids have been found.  Now go through the actors_id_idx pages.
    
    #Open root file
    root_data_d = open('actors_id_idx/root.txt', 'r')
    
    #Add one to total cost and actor index cost
    #obj_1.total_cost_p += 1
    #obj_1.a_idx_p += 1

    #Loop through lines in actor_id_idx root.txt, find proper start leaf file
    row_num_d = 0
    for line_d in root_data_d:
        row_num_d += 1

        if line_d.strip() == '':
            continue

        if line_d.strip() == "internal":
            continue

        root_array_d = [x.strip() for x in line_d.split(',')]

        #Case to handle when there is no minimum actorid set (just pick first leaf node)
        if actorid_low == '*' and row_num_d == 2:
            leaf_location_d = "actors_id_idx/" + root_array_d[1].strip()
            leaf_data_d = open(leaf_location_d, 'r')

            break
        
        #Find actor index leaf file that contains minimum actorid
        if int(actorid_low) <= int(root_array_d[0]):
            leaf_location_d = "actors_id_idx/" + root_array_d[1].strip()
            leaf_data_d = open(leaf_location_d, 'r')

            break
        
    obj_1.total_cost_p += 2 * (len(actorid_set))
    obj_1.a_idx_p += 2 * (len(actorid_set))
    #-------------------------------------------------------------------------------------------------------------------
    #Loop through actor_id_idx files and get needed actor table pages

    row_num_e = 0
    should_break_e = False
    
    leaf_location_e = leaf_location_d
    leaf_data_e = open(leaf_location_e, 'r')
    
    for actorid in actorid_set:
        while (True):
            leaf_data_e.close()
            leaf_data_e = open(leaf_location_e, 'r')
            
            #Add number of table pages needed to total cost and actor table cost
            obj_1.total_cost_p += 1
            obj_1.a_tab_p += 1
            
            for line_e in leaf_data_e:
                row_num_e += 1
        
                if line_e.strip() == '':
                    continue
        
                if line_e.strip() == "leaf":
                    continue
        
                #Open the file at the end of the page and loop on that instead
                if line_e[0] == 'l' and line_e.strip() != "leaf":
                    leaf_location_e = "actors_id_idx/" + line_e.strip()
        
                    obj_1.total_cost_p += 1
                    obj_1.a_idx_p += 1
                    break
        
                leaf_array_e = [x.strip() for x in line_e.split(',')]
                
                if leaf_array_e[0] == actorid:
                
                    #Finally go into actors table and save the chosen actor name
                    page_location_f = "actors_table/" + "page" + leaf_array_e[1] + ".txt"
                    page_data_f = open(page_location_f, 'r')
                    obj_1.a_tab_p += 1
                    
                    for line_f in page_data_f:
                        leaf_array_f = [x.strip() for x in line_f.split(',')]

                        #If actor is a match, add their name to answer set
                        if leaf_array_f[1] == leaf_array_e[0]:
                            name = leaf_array_f[2] + " " + leaf_array_f[3]
                            obj_1.actor_names.add(name)
                            break
                        
                    page_data_f.close()
                    should_break_e = True
                    break
        
                elif leaf_array_e[0] > actorid_high:
                    should_break_e = True
                    break
            
            if should_break_e == True:
                break
    
    return obj_1