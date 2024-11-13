import matplotlib.pyplot as plt
import pandas as pd

file = 'bedload_dataset.txt'
data = pd.read_csv(file)

print(data.head(3))

print("Sum of missing values: " + str(data.isnull().sum()))

print("Sum of duplicated rows: " + str(data.duplicated().sum()))

print(data.describe())

# Morphology section is not in data.describe() because it is a string.

#for column in data.columns:
#    if not "morph" in str(column).lower():
#        data[column].plot(kind='hist')

data["Q"].plot(kind='hist')
plt.show()

for column in data.columns:
    try:
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data[column] < Q1 - 1.5 * IQR) | (data[column] > Q3 + 1.5 * IQR)]
        print('Outliers in column ' + str(column) + ": " + str(outliers))
    except TypeError:
        print(f"Column '{column}' is not numeric.")

# Outliers in slope show that the slope is around 7%, but this is for mountainous regions (we can see Q is small)

import scipy.stats as stats

import numpy as np

numeric_columns = data.select_dtypes(include=[np.number])

# this tells us that all of the results are not normally distributed, which we should expect for a natural dataset
# the p value is very small so we must reject the null hypothesis
normality_results = {}
for column in numeric_columns:
    stat, p_value = stats.shapiro(numeric_columns[column])
    normality_results[column] = {"Statistic:": stat, "p-value:": p_value, "Normality:": p_value > 0.5}

print(normality_results)


def create_qq_plots(df):
    for column in df.columns:
        column_data = df[column].dropna()

        plt.figure()
        stats.probplot(column_data, dist='norm', plot=plt)
        plt.title(f"QQ Plot for {column}")
        plt.xlabel("Theoretical Quantiles")
        plt.ylabel("Sample Quantiles")
        plt.show()


create_qq_plots(numeric_columns)


# We define a list of possible distributions, but we can use the fitter function(?) to automatically fit to
# a distribution. This is Homework !
distributions = ['norm', 'lognorm', 'expon', 'gamma', 'weibull_min']

best_fit_results = {}

for column in numeric_columns:
    column_data = numeric_columns[column].dropna()
    best_fit = {'distribution': None, 'p_value': 0}

    for dist_name in distributions:
        dist = getattr(stats, dist_name)
        params = dist.fit(column_data)

        ks_stat, p_value = stats.kstest(column_data, dist_name, args=params)

        if p_value > best_fit['p_value']:
            best_fit = {'distribution': dist_name, 'p_value': p_value, 'params': params}

    best_fit_results[column] = best_fit

print(best_fit_results)

# This shows that only the U column (velocity) follows a nice gamma distribution.
# Params that are shown are the coefficients that should be used for the distribution.


# this is important to see which parameters are correlated to another param!
spearman_correlation = numeric_columns.corr(method='spearman')
print(spearman_correlation)

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScalar
scaler = StandardScalar()
scaled_data = scaler.fit_transform(numeric_columns)
principal_components = pca.fit_transform(scaled_data)

pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
plt.scatter(pca_df['PC1'], pca_df['PC2'])