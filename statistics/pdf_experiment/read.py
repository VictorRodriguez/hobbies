import pandas as pd
import sys
import matplotlib.pyplot as plt

df = pd.read_csv(sys.argv[1])
df = df.sort_values(by='Count',ascending=False)
df["cumpercentage"] = df["Count"].cumsum()/df["Count"].sum()*100

df_arithmetic = pd.read_csv('arithmetic.csv')
df_branch = pd.read_csv('branch.csv')
df_store = pd.read_csv('store.csv')


df2 = pd.DataFrame(columns=["mnemonic", "Count","cumpercentage"])
for ind in df.index:
    if (df['cumpercentage'][ind]) <= 80:
        df2 = df2.append(df.iloc[ind])
print(df2)
df2.plot(x ='mnemonic', y='Count', kind = 'bar')
plt.show()

arithmetic_counter = (df_arithmetic.mnemonic.isin(df2.mnemonic).sum())
branch_counter = (df_branch.mnemonic.isin(df2.mnemonic).sum())
store_counter = (df_store.mnemonic.isin(df2.mnemonic).sum())
other_counter = len(df2.index) - (arithmetic_counter \
    + branch_counter + store_counter)


data = [['arithmetic', arithmetic_counter],\
        ['branch', branch_counter],\
        ['store_counter', store_counter],\
        ['other_counter', other_counter]]

df_sumary = pd.DataFrame(data, columns = ['InstrKind', 'Times'])
print(df_sumary)
my_labels=['arithmetic','branch','store','other']
df_sumary.plot(labels=my_labels,y='Times',kind='pie',autopct='%1.1f%%')
plt.show()


