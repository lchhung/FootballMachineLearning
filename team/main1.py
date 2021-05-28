import pandas as pd

import glob

def main():

    file_path = glob.glob(r'2016_2017//*.csv')

    list = []
    for file in file_path:
        df = pd.read_csv(file)
        list.append(df)

    final_df = pd.concat(list)
    final_df.reset_index(drop = True, inplace=True)
    final_df.drop('id', axis= 1, inplace= True)
    print(final_df)
    final_df.to_csv("PL_match_team_2016_2017.csv")


    # df = pd.read_csv()




if __name__ == "__main__":
    main()