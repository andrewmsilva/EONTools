from pandas import read_csv

class ModulationLevel:
    def __init__(self, name, data_rate, power_consumption, reach, spectral_efficiency):
        self.name = name
        self.data_rate = data_rate
        self.power_consumption = power_consumption
        self.reach = reach
        self.spectral_efficiency = spectral_efficiency
    
    def __repr__(self):
        return '<%s>'%self.name

    def __str__(self):
        return '<%s>'%self.name

def loadModulationLevels(modulation_levels_csv):
    ml_df = read_csv(modulation_levels_csv)
    
    modulation_levels = []
    for ml in ml_df.iterrows():
        ml = ml[1]
        modulation_levels.append(ModulationLevel(ml['name'], ml['data_rate'], ml['power_consumption'], ml['reach'], ml['spectral_efficiency']))
    
    return modulation_levels