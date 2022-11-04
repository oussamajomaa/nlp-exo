import pandas as pd
import numpy as np
from summarizer import Summarizer

# read csv file
file = pd.read_csv(r'text.csv')
print(file.head())

for index,row in file.iterrows():
    print(row.content)
    print(row.summary)

# model = Summarizer()
# csv_columns = []
# for index,row in file.iterrows():
#     summary = model(row.CONTENT,min_length=10)
#     print(summary)
#     csv_columns.append([row.CONTENT,summary])

# text = pd.DataFrame(csv_columns, columns=['content', 'summary'])
# text.to_csv('text.csv')

# print(csv_columns)