from read_config import ReadConfig

class Simulation:

    def __init__(self,fname):

        self.filename = fname
        config_file = ReadConfig(self.filename)
        dictionary = config_file.get_values()
        
        for key, value in dictionary.iteritems():
            if key == "plat_fname":
                self.plat_fname = value
            if key == "cpu_fname":
                self.cpu_fname = value
            if key == "memory_fname":
                self.memory_fname = value

