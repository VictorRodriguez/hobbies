import json

log = "kcm-0.log"
json_result = "result.json"

data = {}

data['time_unit'] = 's'
data['segments'] = []

# data['segments'].append({
#     'group': 0,
#     'text': 'task 0',
#     'time_start': 10,
#     'time_end': 90
# })


def write_json(data):
    with open(json_result, 'w') as fout:
        json.dump(data, fout)

def time_normalize(date):
    hour    = float(date.split(":")[0])
    minutes = float(date.split(":")[1])
    ms      = (float(date.split(".")[1])/1000)
    seconds = float(date.split(":")[2]) - (ms/1000)

    date_ms = (seconds)*1000 + (minutes)*60000 + (hour*3600000) + ms
    return int(date_ms / 1000) # return in seconds

def main():

    event_id = 0
    start_time = 0.0
    end_time = 0.0

    line = '{:>12}  {:>12}  {:>12} {:>12}'.format("event_id","start_time","end_time","event")
    print(line)

    with open(log, 'r') as fin:
        lines = fin.readlines()
        for line in lines:
            if "E" in line or "I" in line or "W" in line:

                event_id = event_id + 1
                clean_line = line.strip()
                action = (clean_line)

                date = (clean_line.split(" ")[1])
                start_time = (time_normalize(date))
                event = clean_line[30:-1]
                try:
                    next_clean_line = (lines[event_id + 1]).strip()
                except IndexError:
                    next_clean_line = clean_line

                next_date = (next_clean_line.split(" ")[1])
                end_time = (time_normalize(next_date))
                delta = end_time - start_time

                if delta < 0:
                    cp_end_time = end_time
                    end_time = start_time
                    start_time = cp_end_time

                if start_time == end_time:
                    continue
                else:
                    text = "task_%s" % (event_id)
                    data['segments'].append({
                        'group': event_id,
                        'text': "'%s'" % (text),
                        'time_start':start_time,
                        'time_end': end_time
                    })

                    line = '{:>12}  {:>12}  {:>12} {:>20}'.format(event_id,date,next_date,event[0:50])
                    print(line)

    with open('res.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    main()
