import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_DF = '../data.csv'
TRAIN_DF = '../train_10_per.csv'
TEST_DF = '../test_10_per.csv'

PERCENTAGE = 0.10
SPLIT_PERCENTAGE = 0.10

def group_by_labels( df, labels ):
    groups = {}
    for label in labels:
        groups[label] = []
    for _, row in df.iterrows():
        groups[str(row['averageRating'])].append(row)
    return groups

def get_percentage_of_data( data, percentage ):
    _, part = train_test_split( data, test_size=percentage, shuffle=True )
    return part


labels = np.arange(1, 10.1, 0.1)
labels = [ str(round( label, 1 )) for label in labels ]

df = pd.read_csv(INPUT_DF)
df = df.drop(['img_url'], axis = 1) 
columns = df.columns

groups = group_by_labels( df, labels )
reduced_groups = {}
for label in labels:
    reduced_groups[label] = get_percentage_of_data( groups[label], PERCENTAGE )

train_data = []
test_data = []
for group in reduced_groups.values():
    train, test = train_test_split( group, test_size=SPLIT_PERCENTAGE, shuffle=True )
    train_data += train
    test_data += test

train =  pd.DataFrame(train_data, columns = columns)
test =  pd.DataFrame(test_data, columns = columns)

train.to_csv(TRAIN_DF, index = False)
test.to_csv(TEST_DF, index = False)

print( len(df), len(train), len(test) )
