import statistics
import argparse
from pandas import *
from scipy.spatial import distance
import matplotlib.pyplot as plt

def read_data(file_name):
    data = read_csv(file_name)
    instr_ret_any = data['INST_RETIRED.ANY'].tolist()
    return instr_ret_any

def plot_data(data):
    plt.plot(data)
    plt.show()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    data = read_data(args.filename)
    mean = statistics.mean(data)
    stdev = statistics.stdev(data)
    print(mean)
    print(stdev)
    hamming_list = []
    expected_patern = [1] * (len(data))

    for element in data:
        if element > (mean - stdev) and element < (mean + stdev):
            hamming_list.append(1)
        else:
            hamming_list.append(0)
    if len(expected_patern) == len(hamming_list):
        plot_data(hamming_list)
        hd = distance.hamming(expected_patern,hamming_list)
        print(f'Hamming distance vs expected pattern (Lower is better) = {hd}')

if __name__ == "__main__":
    main()

