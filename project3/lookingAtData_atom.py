import pathlib
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import minmax_scale
#from sklearn.preprocessing import StandardsScaler
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import os, random
import numpy as np
import statistics

def select_cells(number_of_cells, filepath):

    dataframes = []
    files = os.listdir(filepath)
    random.seed(6)
    indexes = list(random.randrange(0, len(files)-1, 1) for i in range(number_of_cells))
    print(f'random picked indexes: {indexes}')

    for index in indexes:
        filename= files[index]
        print(filename)
        dataframes.append(pd.read_json(os.path.join(filepath, filename)))

    return dataframes

def select_dataset(df, column):
    # tested for summary column

    if not isinstance(column, (list, tuple)):
        column = [column]

    s = df.loc[:, column]
    print(f"Shape of selected packed dataset: {s.shape}")

    s = s.dropna()
    print(f"Shape of selected packed dataset without NaNs: {s.shape}")
    if s.empty:
        print("Non values found")
        return

    s = s.T.apply(pd.Series.explode).set_index("cycle_index")
    print(f"Shape of selected unpacked dataset: {s.shape}")

    return s

# Creates list of dataframes containing battery data files
cells = select_cells(10, pathlib.Path("/Users/Andreas/Documents/Data"))

# Ignore files with cycle life less than 150 and create list of dataframes
# with summary data (per cycle) and full cycling data.
df_summaries = []
df_cycles = []
for cell in cells:
    if select_dataset(cell, 'summary').index[-1] > 149:
        df_summaries.append(select_dataset(cell, 'summary'))

        cycle = select_dataset(cell, 'cycles_interpolated')
        #cycle = cycle.dropna()
        df_cycles.append(cycle)

print(len(df_summaries))
print(len(df_cycles))
