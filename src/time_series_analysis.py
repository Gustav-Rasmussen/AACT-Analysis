
from src.static_analysis import get_conditions_df, get_country_df, get_combined_df
import pandas as pd
import glob
from pprint import pprint as pp
# from datetime import datetime
from tqdm import tqdm

condition_files = glob.glob("data_curated/conditions/conditions_*.csv")
country_files = glob.glob("data_curated/countries/countries_*.csv")

dates = [file[-12:-4] for file in condition_files]
# pp(dates)
# f_conditions = condition_files[0]
# f_countries = country_files[0]

date_and_val = []
for date, f_conditions, f_countries in tqdm(zip(dates, condition_files, country_files)):
    df_conditions = get_conditions_df(f_conditions)
    df_countries = get_country_df(f_countries)

    df_combined = get_combined_df(df_conditions, df_countries)
    print(df_combined.head(1))
    unique_cond = list(df_combined.CONDITION.unique())
    # pp(unique_cond)
    '''
    for cond in unique_cond:
        if (('diabetes' in cond)
                and (("type 2" in cond) or ("type two" in cond))
                and ("type 1" not in cond)):
            print(cond)
    '''
    df_cond_freq = df_combined.groupby('CONDITION').count()
    # number_of_cases = 1_000
    # cond_freq_filt = (df_cond_freq.NCT_ID > number_of_cases)
    # df_most_freq = df_cond_freq[cond_freq_filt]
    df_most_freq = df_cond_freq.sort_values(['NCT_ID'])
    #df_most_freq = df_most_freq.reset_index()
    # print(df_most_freq)

    num_people = sum(df_most_freq['NCT_ID'])
    qty = df_most_freq['NCT_ID']['obesity']  #  / num_people
    # qty = df_most_freq['NCT_ID']['breast cancer']  # / num_people
    date_and_val.append([date, num_people])  # qty


df = pd.DataFrame(date_and_val, columns=["Date", "Obesity"])

print(df)

df.to_csv("Obesity_time_series.csv")

def main():
    pass


if __name__ == "__main__":
    main()

    # filt_obesity = df_most_freq.CONDITION == "obesity"
    # filt_diabetes = df_most_freq.CONDITION == "diabetes melittus, type 2"
