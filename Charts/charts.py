import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Users_ProgExp.csv')
# print(df)
df.plot.bar(x = 'Where The Users Gained Programming Experience', y = 'Number of Users')
