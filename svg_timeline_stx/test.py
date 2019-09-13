import json

data = {}

data["time_unit"] = "ms"
data['segments'] = []
data['segments'].append({
    'group': 0,
    'text': 'task 0',
    'time_start': 10,
    'time_end': 90
})

data['segments'].append({
    'group': 1,
    'text': 'task 1',
    'time_start': 15,
    'time_end': 60
})

data['segments'].append({
    'group': 2,
    'text': 'task 2',
    'time_start': 65,
    'time_end': 80
})
#time_unit = {"time_unit":"ms"}

with open('in.json', 'w') as fout:
    json.dump(data, fout)


