import pandas as pd
import plotly.express as px

df_h = pd.read_csv("histogram.csv")
df_db = pd.read_json("presibuilds.intrinsics.json")
df_data = pd.DataFrame(columns=['instruction', 'technology', 'count'])

for instruction in df_db['instruction']:
        df_tech=df_db[df_db['instruction']==instruction]['technology']
        df_platform=df_db[df_db['instruction']==instruction]['platforms']
        if not df_tech.empty:
            string = (list(dict.fromkeys(df_tech.tolist())))
            technology = ('_'.join(string))
            if any(df_platform.tolist()):
                platforms_ = (list(dict.fromkeys(df_platform.tolist()[0])))
                platforms = ('_'.join(platforms_))
            else:
                platforms = "x86"
            if instruction.lower() in df_h['Mnemonic'].values:
                tmp =  df_h[df_h['Mnemonic'] == instruction.lower()]['Count']
                count = ([int(x) for x in tmp.tolist()][0])
            else:
                count = 0
            new_row = pd.DataFrame({'instruction':instruction.lower(), 'technology':technology, 'count':count, 'platforms': platforms}, index=[0])
            df_data = pd.concat([df_data, new_row], axis=0, ignore_index=True)

print(df_data)

fig = px.sunburst(df_data, path=['platforms','technology', 'instruction', 'count'], values = 'count')
fig.show()

