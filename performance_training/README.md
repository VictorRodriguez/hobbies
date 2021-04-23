# Perf training


1 Build

```
make
```

2 Check the record and see if match

```
perf report
```

3 Draw the graph to visualize

```
make graph
```
## TODO

http://sandsoftwaresound.net/perf/perf-tutorial-hot-spots/

In order to generate a log easy to parse:

'''
perf report --stdio > log
'''
