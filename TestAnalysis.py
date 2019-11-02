from pandas import read_csv, concat
from glob import glob
from EONTools import Figure

# Reading all simulations
all_files = glob('results/*.csv')
simulations = []
for filename in all_files:
    df = read_csv(filename, index_col=None, header=0)
    simulations.append(df)
simulations = concat(simulations, axis=0, ignore_index=True)

Figure.formatLabels(simulations)
print(simulations.describe())

# Calculating correlations
corr = simulations.corr()

# Plotting heatmap
Figure.clearBuffer()
Figure.heatmap(corr)
Figure.plot()

# Plotting barplot
Figure.clearBuffer()
Figure.bar(corr['Block Rate'])
Figure.plot()