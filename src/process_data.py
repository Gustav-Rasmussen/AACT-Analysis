import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_sick_df():
    f = r"etl_folder/conditions/conditions_20200601.csv"
    df_conditions = pd.read_csv(f).drop(columns=["Unnamed: 0"]).rename(columns={'downcase_name': 'CONDITION',
                                                                                'nct_id': 'NCT_ID'
                                                                                })
    # print(df_conditions.head())
    # Get unique conditions
    # print(df_conditions.CONDITION.unique())
    filt = df_conditions.CONDITION != "Healthy"
    df_sick = df_conditions[filt]
    # Count frequencies of conditions
    df_cond_freq = df_sick.groupby('CONDITION').count()
    # print(df_cond_freq.tail())
    return df_sick


def get_country_df():
    f = r"etl_folder/countries/countries_20200601.csv"
    df_countries = pd.read_csv(f).drop(columns=["Unnamed: 0"]).rename(columns={'name': 'COUNTRY', 'nct_id': 'NCT_ID'})
    # Get unique countries, slice first 5
    # print(df_countries.COUNTRY.unique()[:5])
    # Count frequencies of countries
    df_c_freq = df_countries.groupby('COUNTRY').count()
    # print(df_c_freq.tail())
    # Get most common countries, with over one thousand cases in terms of either CONDITION_ID or NCT_ID
    c_freq_filt = df_c_freq.NCT_ID > 10_000
    df_c_most_freq = df_c_freq[c_freq_filt]
    df_c_most_freq = df_c_most_freq.sort_values(['NCT_ID'])
    # print(df_c_most_freq)
    return df_countries


def get_combined_df(df_sick, df_countries):
    df_combined = df_sick.merge(df_countries)
    # print(df_combined.head())
    # Count frequencies of conditions
    df_cond_freq = df_combined.groupby('CONDITION').count()
    # df_combined = df_combined.groupby(['COUNTRY', 'CONDITION']).size()
    # df_combined = df_combined.groupby(['COUNTRY', 'CONDITION']).size().groupby(level=0).max()
    # df_combined = df_combined.groupby(['COUNTRY', 'CONDITION']).size().reset_index().groupby('COUNTRY')[[0]].max()
    # print(df_cond_freq.head())
    # Get most common conditions in terms of NCT_ID
    number_of_cases = 3_500
    cond_freq_filt = (df_cond_freq.NCT_ID > number_of_cases)
    df_most_freq = df_cond_freq[cond_freq_filt]
    df_most_freq = df_most_freq.sort_values(['NCT_ID'])
    # print(df_most_freq)
    return df_most_freq


def get_combined_df_us(df_sick, df_countries):
    df_combined = df_sick.merge(df_countries)
    us_filt = df_combined.COUNTRY == "United States"
    df_combined_us = df_combined[us_filt]
    # print(df_combined_us.head())
    df_cond_freq = df_combined_us.groupby('CONDITION').count()
    number_of_cases = 1_000
    cond_freq_filt = (df_cond_freq.NCT_ID > number_of_cases)
    df_most_freq_us = df_cond_freq[cond_freq_filt]
    df_most_freq_us = df_most_freq_us.sort_values(['NCT_ID'])
    print(df_most_freq_us)
    return df_most_freq_us


def show_top_conditions(df_most_freq):
    """Show the most common condition."""
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=df_most_freq.reset_index(),
                     x="CONDITION",
                     y="NCT_ID"
                    )
    ax.axes.set_title("AACT project - most common conditions 2020", fontsize=25)
    l = ax.set_xticklabels(ax.get_xticklabels(), rotation=75, fontsize=15)
    ax.set_xlabel("Condition", fontsize=20)
    ax.set_ylabel("Counts", fontsize=20)
    plt.tight_layout()
    plt.savefig('img/most_common_conditions.png')


def show_top_conditions_us(df_most_freq_us):
    """Show the most common conditions for US."""
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=df_most_freq_us.reset_index(),
                     x="CONDITION",
                     y="NCT_ID"
                     )
    ax.axes.set_title("AACT project - most common conditions 2020 - US", fontsize=25)
    l = ax.set_xticklabels(ax.get_xticklabels(), rotation=75, fontsize=15)
    ax.set_xlabel("Condition", fontsize=20)
    ax.set_ylabel("Counts", fontsize=20)
    plt.tight_layout()
    plt.savefig('img/most_common_conditions_us.png')


def main():
    df_sick = get_sick_df()
    df_countries = get_country_df()

    df_most_freq = get_combined_df(df_sick, df_countries)
    show_top_conditions(df_most_freq)

    df_most_freq_us = get_combined_df_us(df_sick, df_countries)
    show_top_conditions_us(df_most_freq_us)

    plt.show()


if __name__ == "__main__":
    main()
