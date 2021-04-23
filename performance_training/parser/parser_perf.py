file1 = open('log', 'r')
Lines = file1.readlines()

list_events = []
perf_event = {}

for line in Lines:
    if not line.startswith("#") and line != "\n":
        line_split = ((line.strip().split("  ")))
        perf_event = dict(
            Overhead=line_split[0],
            Command=line_split[1],
            SharedObject=line_split[2],
            Symbol=line_split[3:4]
            )
        print(perf_event)

