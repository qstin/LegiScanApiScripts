import os
import pandas as pd

for i in os.listdir(os.getcwd()):
    if i.endswith(".csv"):
        df = pd.read_csv(i)
        if df['score'].max() >= 100:
            print(i)
        except KeyError:
            pass

