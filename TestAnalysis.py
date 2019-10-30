from pandas import read_csv
from EONTools import Figure

simulations = read_csv('results/test0.csv')
corr = simulations.corr()

print(simulations.describe())
print(corr['block_rate'])

Figure.clearBuffer()
Figure.heatmap(corr)
Figure.plot()

Figure.clearBuffer()
Figure.bar(corr['block_rate'])
Figure.plot()