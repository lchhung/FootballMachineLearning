import glob
import time

import json_lines

import json


# To run, type: python main.py
import csv
import pprint as pp
import pandas as pd

from methods import retrievePlayerAttributes

start = time.time()

def main():


    file_path = glob.glob(r'data//2015_2016//*.jsonlines')

    list = []
    num = 12
    for file_name in file_path:
        print(file_name)
        with open('data//2015_2016//2015_09.jsonlines', "rb") as f:
            obj = json_lines.reader(f)

            player_list = []
            while num > 0:
                item = next(obj)
                # print(item)
                # print(len(item))
                player_list.append(item)
                num = num - 1

                for content in player_list:
                    df = pd.DataFrame(content)
                    print(df)


            # print(df.shape)

            # print(player_list)


if __name__ == "__main__":
    main()

print("\n" + 40 * "#")
print(time.time() - start)
print(40 * "#" + "\n")