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

# cpu
print("CPU name: %s" % sim.cpu_name)

# memories kind
print("Memories kind: %s" % sim.memories_kind)

# memories kind
print("Memories size: %s" % sim.memories_size)

# memories kind
print("Memories brand: %s" % sim.memories_brand)
