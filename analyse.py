from pandas import read_csv, concat
from glob import glob
from EONTools import Figure

# Loading simulations
all_files = glob('results/simulate_all/*.csv')
simulations = []
for filename in all_files:
    df = read_csv(filename, index_col=0)
    simulations.append(df)
simulations = concat(simulations)

# Beautifying labels
simulations.columns = [column.replace("_", " ").title() for column in simulations.columns]
print(simulations.describe())

# Casting columns
for i in range(len(simulations.columns)):
  if simulations.dtypes[i] != 'float64' or simulations.dtypes[i] != 'int64':
    simulations[simulations.columns[i]] = simulations[simulations.columns[i]].astype(float)

# Calculating correlations
corr = simulations.corr(min_periods=8)
print(corr)

# Plotting results
ax = Figure.heatmap(corr)
ax.set_title('Correlation matrix')
Figure.show()

ax = Figure.bar(corr['Blocking Coefficient'])
ax.set_title('Correlation by Blocking Coefficient')
Figure.show()

# Figure.sns.pairplot(simulations, palette=Figure.palette)
# Figure.show()