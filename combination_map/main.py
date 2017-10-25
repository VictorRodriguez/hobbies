from src.platform import Platform
from src.simulation import Simulation



# Read simulation file to get system and rules information
sim_fname = "simulations/sim_NUC.txt"
sim = Simulation(sim_fname)

# platform
platform = Platform(sim.plat_fname)

print("Platform Name: %s" % sim.plat_name)
print("Platform Kind: %s" % platform.kind)
print("Platform Model: %s" % platform.model)
print("# soquets: %s" % platform.no_soquets)
print("# memo dims: %s" % platform.no_mem_dims)
print("# sata dims: %s" % platform.no_sata_dims)
print("# oculink ports: %s" % platform.no_oculink_ports)

# cpu
print("CPU name: %s" % sim.cpu_name)

# memories kind
print("Memories kind: %s" % sim.memories_kind)

# memories kind
print("Memories size: %s" % sim.memories_size)

# memories kind
print("Memories brand: %s" % sim.memories_brand)


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

