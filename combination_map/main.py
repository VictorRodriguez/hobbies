from src.platform import Platform
from src.simulation import Simulation
from src.read_config import ReadConfig
import argparse
import os.path
import sys

# create trees of slots of cpu 
# create trees of slots of mmeory 
# create trees of slots of HD
#
# each leave of teh tree will have a conection to the next tree kind
#
# that will link to all the posibilities of sub threas that you coudl have 
#
# after the threa is conected 
# then calculate all the posibilities
# rules is cleaning all the leaves that do not apply in a fast way

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
        print(sim_files)
    else:
        print("ERROR: File %s does not exist",sim_file)
        sys.exit(-1)

    for comp,file_path in sim_files.items():
        if os.path.isfile(file_path):
            # create array of dictionaries to combine
            db_obj = ReadConfig(file_path)
            db_obj.load_db_values()
            print(comp)
            print(file_path)
            print(db_obj.get_comp_items())
        else:
            print("WARNING: File %s does not exist",file_path)
            pass

    # combine and create tree
    #


    # apply rules, walk over teh tree as fast as possible
    #

