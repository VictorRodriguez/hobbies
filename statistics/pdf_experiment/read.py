import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(sys.argv[1])
df = df.sort_values(by='Count',ascending=False)
df["cumpercentage"] = df["Count"].cumsum()/df["Count"].sum()*100
df["pro"] = df["Count"]/df["Count"].sum()


df.head(11).plot(x ='mnemonic', y='pro', kind = 'bar')
plt.show()

df_arithmetic = pd.read_csv('arithmetic.csv')
df_branch = pd.read_csv('branch.csv')
df_store = pd.read_csv('store.csv')


#df_prob = df.assign(pro=df.Count.map(df.Count.value_counts(normalize=True)))
#print(df_prob)
#ax = df.Count.plot(kind='hist')
#df.Count.plot(kind='kde', ax=ax, secondary_y=True)
#plt.show()

df2 = pd.DataFrame(columns=["mnemonic", "Count","cumpercentage"])
for ind in df.index:
    if (df['cumpercentage'][ind]) <= 80:
        df2 = df2.append(df.iloc[ind])

#print(df2)
#df2.plot(x ='mnemonic', y='Count', kind = 'bar')
#plt.show()

arithmetic_counter = (df_arithmetic.mnemonic.isin(df2.mnemonic).sum())
branch_counter = (df_branch.mnemonic.isin(df2.mnemonic).sum())
store_counter = (df_store.mnemonic.isin(df2.mnemonic).sum())
other_counter = len(df2.index) - (arithmetic_counter \
    + branch_counter + store_counter)

df_a = df2[df2.mnemonic.isin(df_arithmetic.mnemonic)]
df_b = df2[df2.mnemonic.isin(df_branch.mnemonic)]
df_s = df2[df2.mnemonic.isin(df_store.mnemonic)]
df_o = pd.concat([df2,df_a, df_b, df_s]).drop_duplicates(keep=False)

#print(df_o)

data = [['arithmetic', arithmetic_counter],\
        ['branch', branch_counter],\
        ['store_counter', store_counter],\
        ['other_counter', other_counter]]

#df_sumary = pd.DataFrame(data, columns = ['InstrKind', 'Times'])
#print(df_sumary)

data_count = [['arithmetic', df_a['Count'].sum()],\
        ['branch', df_b['Count'].sum()],\
        ['store_counter', df_s['Count'].sum()],\
        ['other_counter', df_o['Count'].sum()]]

df_sumary = pd.DataFrame(data_count, columns = ['InstrKind', 'Times'])
my_labels=['arithmetic','branch','store','other']
df_sumary.plot(labels=my_labels,y='Times',kind='pie',autopct='%1.1f%%')
#plt.show()


