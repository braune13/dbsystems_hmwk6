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

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1
            break
        #Find internal node that contains minimum movieid
        elif int(movieid_low) <= int(root_array[0]):
            internal_location = "movieroles_ma_idx/" + root_array[2]
            internal_data = open(internal_location, 'r')

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1
            break


    #-------------------------------------------------------------------------------------------------------------------
    #Loop through lines in internal file, find leaf node that contains minimum movieid
    row_num = 0
    for line in internal_data:
        row_num += 1
        if line.strip() == "internal":
            continue

        internal_array = [x.strip() for x in line.split(',')]

        #Case to handle where there is no minimum movieid set (just pick first internal node)
        if movieid_low == '*' and row_num == 2:
            leaf_location = "movieroles_ma_idx/" + internal_array[2].strip()
            leaf_data = open(leaf_location, 'r')

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1

            break
        elif int(movieid_low) <= int(internal_array[0]):
            leaf_location = "movieroles_ma_idx/" + internal_array[2]
            leaf_data = open(leaf_location, 'r')

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1
            break
    #-------------------------------------------------------------------------------------------------------------------
    #Loop through lines in leaf file(s), add matching actorids to a set
    actorid_set = set()
    for line in leaf_data:

        if line.strip() == '':
            continue

        if line.strip() == "leaf":
            continue

        if (line.strip())[0] == 'l' and line.strip() != "leaf":
            leaf_location = "movieroles_ma_idx/" + line.strip()
            print leaf_location
            leaf_data = open(leaf_location, 'r')

            obj_1.total_cost_p += 1
            obj_1.mr_idx_p += 1

            continue

        leaf_array = [x.strip() for x in line.split(',')]

        #Stop searching through leaf when movieid > movieid_high
        if movieid_high != '*' and leaf_array[0] > movieid_high:
            break

        #If actorid is in specified range, add actorid to actorid_set
        elif ((actorid_low != '*' and leaf_array[1] >= actorid_low) or actorid_low == '*') and ((actorid_high != '*' and leaf_array[1] <= actorid_high) or actorid_high == '*'):
            actorid_set.add(leaf_array[1])
    #-------------------------------------------------------------------------------------------------------------------
    #All actorids have been found.  Now go through the actors_id_idx pages.

    print "Number of matching actor id's found: " + str(len(actorid_set))
    #Open root file
    root_data = open('actors_id_idx/root.txt', 'r')

    #Add one to total cost and a_idx_p to account for root file
    obj_1.total_cost_p += 1
    obj_1.a_idx_p += 1

    #-------------------------------------------------------------------------------------------------------------------
    #Loop through lines in actor_id_idx root.txt, find proper start leaf file

    row_num = 0
    for line in root_data:
        row_num += 1

        if line.strip() == '':
            continue

        if line.strip() == "internal":
            continue

        root_array = [x.strip() for x in line.split(',')]

        # Case to handle when there is no minimum actorid set (just pick first leaf node)
        if actorid_low == '*' and row_num == 2:
            leaf_location = "actors_id_idx/" + root_array[1].strip()
            leaf_data = open(leaf_location, 'r')

            # Add one to total cost and actor index cost
            obj_1.total_cost_p += 1
            obj_1.a_idx_p += 1
            break
        elif int(actorid_low) <= int(root_array[0]):
            leaf_location = "actors_id_idx/" + root_array[1].strip()
            leaf_data = open(leaf_location, 'r')

            obj_1.total_cost_p += 1
            obj_1.a_idx_p += 1
            break
    #-------------------------------------------------------------------------------------------------------------------
    #Loop through actor_id_idx files and get needed actor table pages

    row_num = 0
    actor_table_pages = set()
    for line in leaf_data:
        row_num += 1

        if line.strip() == '':
            continue

        if line.strip() == "leaf":
            continue

        #Open the file at the end of the page and loop on that instead
        if line[0] == 'l' and line.strip() != "leaf":
            leaf_location = "actors_id_idx/" + line.strip()
            leaf_data = open(leaf_location, 'r')

            obj_1.total_cost_p += 1
            obj_1.a_idx_p += 1

            continue

        leaf_array = [x.strip() for x in line.split(',')]

        if leaf_array[0] in actorid_set:
            actor_table_pages.add(leaf_array[1])

        elif leaf_array[0] > actorid_high:
            break

    #Add number of table pages needed to total cost and actor table cost
    obj_1.total_cost_p += len(actor_table_pages)
    obj_1.a_tab_p += len(actor_table_pages)

    #-------------------------------------------------------------------------------------------------------------------
    #FINALLY go into actors table and save the chosen actor names
    print actor_table_pages
    for page in actor_table_pages:
        page_location = "actors_table/" + "page" + page + ".txt"
        page_data = open(page_location, 'r')

        for line in page_data:
            leaf_array = [x.strip() for x in line.split(',')]

            #If actor is a match, add their name to answer set
            if leaf_array[1] in actorid_set:
                name = leaf_array[2] + " " + leaf_array[3]
                obj_1.actor_names.add(name)
    #-------------------------------------------------------------------------------------------------------------------
    return obj_1


#=======================================================================================================================