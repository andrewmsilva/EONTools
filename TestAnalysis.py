from pandas import read_csv, concat
from glob import glob
from EONTools import Figure

# Reading all simulations
all_files = glob('results/*.csv')
simulations = []
for filename in all_files:
    df = read_csv(filename)
    simulations.append(df)
simulations = concat(simulations, axis=0, ignore_index=True)

Figure.formatLabels(simulations)
print(simulations.describe())

# Calculating correlations
corr = simulations.corr()

# Plotting
fig, ax = Figure.subplots(1, 2)

ax[0].set_title('Correlation matrix')
Figure.heatmap(corr, ax[0])

ax[1].set_title('Correlation by Block Rate')
Figure.bar(corr['Block Rate'], ax[1])

Figure.show()