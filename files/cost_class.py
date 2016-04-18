# CostData class to hold cost information for each method run ... also holds set of actor names found from query

class CostData:
    def __init__(self):
        self.total_cost_p = 0
        self.mr_idx_p = 0
        self.mr_tab_p = 0
        self.a_idx_p = 0
        self.a_tab_p = 0

        self.actor_names = set()
