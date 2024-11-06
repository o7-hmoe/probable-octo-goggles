import pandas as pd

from plot_discharge import plot_discharge



# load data
df = pd.read_csv("flow-data/daily-flow-series.csv",
                 header=36,
                 sep=";",
                 names=["Date", "Q (CMS)"],
                 usecols=[0, 2],
                 parse_dates=[0],
                 index_col="Date")
print(df.head())

plot_discharge(df.index,df["Q (CMS)"], title="Daily Flow Data")

annual_max_df = df.resample(rule="YE", kind="period").max()
annual_max_df["year"] = annual_max_df.index.year
annual_max_df.reset_index(inplace=True, drop=True)
print(annual_max_df.head())
plot_discharge(annual_max_df["year"], annual_max_df["Q (CMS)"], title="Wasserburg a. Inn 1826 - 2016 (annual)")

annual_max_df_sorted = annual_max_df.sort_values(by="Q (CMS)")

n = annual_max_df_sorted.shape[0]
annual_max_df_sorted.insert(0, "rank", range(1, 1 + n))

annual_max_df_sorted["pr"] = (n - annual_max_df_sorted["rank"] + 1) / (n + 1)

annual_max_df_sorted["return-period"] = 1 / annual_max_df_sorted["pr"]

print(annual_max_df_sorted.tail())

from plot_result import plot_q_freq, plot_q_return_period

plot_q_freq(annual_max_df_sorted)
plot_q_return_period(annual_max_df_sorted)