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

def time_normalize(date):
    hour    = float(date.split(":")[0])
    minutes = float(date.split(":")[1])
    ms      = (float(date.split(".")[1])/1000)
    seconds = float(date.split(":")[2]) - (ms/1000)

    date_ms = (seconds)*1000 + (minutes)*60000 + (hour*3600000) + ms
    return date_ms

def main():

    event_id = 0
    start_time = 0.0
    end_time = 0.0

    with open(log, 'r') as fin:
        lines = fin.readlines()
        for line in lines:
            if "E" in line or "I" in line or "W" in line:

                event_id = event_id + 1
                clean_line = line.strip()
                action = (clean_line)

                date = (clean_line.split(" ")[1])
                start_time = (time_normalize(date))

                try:
                    next_clean_line = (lines[event_id + 1]).strip()
                except IndexError:
                    next_clean_line = clean_line

                next_date = (next_clean_line.split(" ")[1])
                end_time = (time_normalize(next_date))

                delta = end_time - start_time
                print("%d   %s : %s :  %s" % (event_id,date,next_date,delta))

if __name__ == "__main__":
    main()
