from src.platform import Platform
from src.simulation import Simulation
from src.read_config import ReadConfig
import argparse
import os.path
import sys
import pprint
import numpy as np

if __name__ == "__main__":

    sim_file = "simulations/sim_NUC.txt"

    parser = argparse.ArgumentParser(description='This is a Combinational tool\
            for validation systems')
    parser.add_argument('--simulation_file',dest="sim_file",type=file)
    args = parser.parse_args()

    if args.sim_file:
        sim_file = args.sim_file

    # Read simulation file to get system and rules information
    if os.path.isfile(sim_file):
        sim_obj = ReadConfig(sim_file)
        sim_obj.load_simulation_values()
        sim_files = sim_obj.get_sim_files()
    else:
        print("ERROR: File %s does not exist",sim_file)
        sys.exit(-1)

    # main db 
    db_dic = {}

    #array of size of elements per component
    comp_len_array = []

    for comp,file_path in sim_files.items():
        if os.path.isfile(file_path):
            # create array of dictionaries to combine
            db_obj = ReadConfig(file_path)
            db_obj.load_db_values()
            comp_len_array.append(len(db_obj.get_comp_items()))
            # put the array in a dictionary to don't loose it
            db_dic[comp] = db_obj.get_comp_items()

        else:
            print("WARNING: File %s does not exist",file_path)
            pass

    pprint.pprint(db_dic)

    # combine and create tree
    combination = np.array(np.meshgrid(*[np.arange(1, x+1) for x in \
            comp_len_array])).T.reshape(-1,len(comp_len_array))

    print(combination)

    # apply rules, walk over teh tree as fast as possible
    #
