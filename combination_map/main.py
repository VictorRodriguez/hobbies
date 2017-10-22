from src.platform import Platform
from src.simulation import Simulation



# Read simulation file to get system and rules information

sim_fname = "simulations/sim_NUC.txt"
sim = Simulation(sim_fname)

# platform
platform = Platform(sim.plat_fname)
print(platform.kind)

# memory
# cpu

