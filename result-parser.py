import os
import re
import pandas as pd


def find_high_results():

    regex = re.compile(r'[!^"az"]')
    match_counter = 0

    for i in os.listdir(os.getcwd()):
        if i.endswith(".csv"):
            df = pd.read_csv(i)
            for index, row in df.iterrows():
                if not regex.match(row['doc_id']):
                    if row['score'] >= 75:
                        match_counter += 1
                    print(i + " contains " + match_counter + 
                            " out-of-state matches")
            except KeyError:
                pass

