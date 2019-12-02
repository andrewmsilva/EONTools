from pandas import read_csv, concat
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt

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

# Creating palette for plots
palette = sns.diverging_palette(220, 20, n=200)

# Pairplot
# sns.pairplot(simulations, palette=palette)
# plt.show()

# Correlation matrix heatmap
ax = sns.heatmap(
  corr,
  center=0,
  cmap=palette,
  square=True,
  annot=True,
)
ax.set_xticklabels(
  ax.get_xticklabels(),
  rotation=45,
  horizontalalignment='right'
)
ax.set_title('Correlation matrix heatmap')
plt.show()

# Blocking Coefficient correlations bar plot
ax = sns.barplot(
  x=corr['Blocking Coefficient'].index,
  y=corr['Blocking Coefficient'].values,
  palette=palette,
)
ax.set_xticklabels(
  ax.get_xticklabels(),
  rotation=45,
  horizontalalignment='right'
)
ax.set_title('Correlation by Blocking Coefficient')
plt.show()