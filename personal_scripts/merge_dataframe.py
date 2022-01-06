import pandas as pd

file_1 = "~/Downloads/total_with_no_prints_no_tmul_1.csv"
file_2 = "~/Downloads/total_with_no_prints_no_tmul_2.csv"
df_1 = pd.read_csv(file_1)
df_2 = pd.read_csv(file_2)

print(df_1)
print(df_2)

df = df_1.set_index('mnemonic').add(df_2.set_index('mnemonic'), fill_value=0).reset_index()
print (df.sort_values('Count'))
file_name="out.csv"
df.to_csv(file_name, sep=',', encoding='utf-8')
