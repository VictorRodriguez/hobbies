import json

log = "kcm-0.log"
json_result = "result.json"

data = {}

data["time_unit"] = "ms"
data['segments'] = []
data['segments'].append({
    'group': 0,
    'text': 'task 0',
    'time_start': 10,
    'time_end': 90
})

def write_json(data):
    with open(json_result, 'w') as fout:
        json.dump(data, fout)

def main():
    with open(log, 'r') as fin:
        lines = fin.readlines()
        for line in lines:
            if "E" in line or "I" in line or "W" in line:
                clean_line = line.strip()
                print(clean_line.split(" ")[1])

if __name__ == "__main__":
    main()
