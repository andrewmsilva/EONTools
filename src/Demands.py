class Demands(list):
    def __init__(self):
        self.exectable = None
        self.active = True
        self.error = False
    
    def add(self, source, target, data_rate):
        demand_id = len(self)
        self.append({
            'from': source, 
            'to': target,
            'data_rate': data_rate,
            'nodes_path': None,
            'links_path': None,
            'path_length': None,
            'modulation_format': None,
            'frequency_slots': None,
            'spectrum_path': None,
            'status': self.exectable,
        })
        return demand_id