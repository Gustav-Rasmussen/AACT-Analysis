import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from pprint import pprint as pp

if not os.path.isdir("logs"):
    os.mkdir("logs")

logging.basicConfig(level=logging.INFO,
                    filename='logs/app.log',
                    filemode='w',
                    format='%(levelname)s - %(message)s'
                    )

logging.info('Starting program: process_data')


# Normalize by number of participants every month


def get_conditions_df(f="data_curated/conditions/conditions_20200601.csv"):
    df_conditions = pd.read_csv(f).drop(columns=["Unnamed: 0"]).rename(columns={'downcase_name': 'CONDITION',
                                                                                'nct_id': 'NCT_ID',
                                                                                'name': 'CONDITION',
                                                                                })
    # logging.info(df_conditions.head())
    # Get unique conditions
    # logging.info(df_conditions.CONDITION.unique())
    # filt = df_conditions.CONDITION != "Healthy"
    # df_sick = df_conditions[filt]
    # Count frequencies of conditions
    # df_cond_freq = df_sick.groupby('CONDITION').count()
    # logging.info(df_cond_freq.tail())
    return df_conditions  # df_sick


def get_country_df(f="data_curated/countries/countries_20200601.csv"):
    df_countries = pd.read_csv(f).drop(columns=["Unnamed: 0"]).rename(columns={'name': 'COUNTRY', 'nct_id': 'NCT_ID'})
    # Get unique countries, slice first 5
    # logging.info(df_countries.COUNTRY.unique()[:5])
    # Count frequencies of countries
    # df_c_freq = df_countries.groupby('COUNTRY').count()
    # logging.info(df_c_freq.tail())
    # Get most common countries, with over one thousand cases in terms of either CONDITION_ID or NCT_ID
    # c_freq_filt = df_c_freq.NCT_ID > 10_000
    # df_c_most_freq = df_c_freq[c_freq_filt]
    # df_c_most_freq = df_c_most_freq.sort_values(['NCT_ID'])
    # logging.info(df_c_most_freq)
    return df_countries


def get_combined_df(df_1, df_2, country_filt="United States"):
    df_combined = df_1.merge(df_2)
    country_filter = df_combined.COUNTRY == country_filt
    df_combined = df_combined[country_filter]
    return df_combined


def show_top_conditions(df_most_freq, country_filt="United States"):
    """Show the most common conditions for US."""
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=df_most_freq.reset_index(),
                     x="CONDITION",
                     y="NCT_ID"
                     )
    ax.axes.set_title(f"AACT project - most common conditions 2020 - {country_filt}", fontsize=25)
    l = ax.set_xticklabels(ax.get_xticklabels(), rotation=75, fontsize=15)
    ax.set_xlabel("Condition", fontsize=20)
    ax.set_ylabel("Counts", fontsize=20)
    plt.tight_layout()
    plt.savefig('img/most_common_conditions_us.png')


def main():
    # df_sick = get_sick_df()
    df_conditions = get_conditions_df()
    for cond in df_conditions.CONDITION.unique():
        if 'obesity' in cond:
            print(cond)
    # pp(df_conditions.CONDITION.unique())
    # unique_cond = df_conditions.CONDITION.unique()
    # pp(unique_cond)
    # print(df_sick.head())
    # df_countries = get_country_df()
    # print(df_countries.head())
    # df_most_freq = get_combined_df(df_conditions, df_countries)
    # show_top_conditions(df_most_freq)
    # plt.show()


if __name__ == "__main__":
    main()
