from pandas import read_csv, concat
from glob import glob
from EONTools import Figure

# Loading simulations
all_files = glob('results/*.csv')
simulations = []
for filename in all_files:
    df = read_csv(filename, index_col=0)
    simulations.append(df)
simulations = concat(simulations)

# Beautifying labels
simulations.columns = [column.replace("_", " ").title() for column in simulations.columns]
print(simulations.describe())

# Calculating correlations
corr = simulations.corr()
print(corr)

# Plotting results
ax = Figure.heatmap(corr)
ax.set_title('Correlation matrix')
Figure.show()

ax = Figure.bar(corr['Block Rate'])
ax.set_title('Correlation by Block Coefficient')
Figure.show()