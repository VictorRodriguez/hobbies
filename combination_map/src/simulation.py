from read_config import ReadConfig

class Simulation:

    def __init__(self,fname):

        self.filename = fname
        config_file = ReadConfig(self.filename)
        dictionary = config_file.get_values()
        
        for key, value in dictionary.iteritems():
            if key == "plat_name":
                self.plat_name = value
            if key == "plat_fname":
                self.plat_fname = value
            if key == "cpu_name":
                self.cpu_name = value
            if key == "cpu_fname":
                self.cpu_fname = value
            if key == "memories_kind":
                self.memories_kind = value
            if key == "memories_size":
                self.memories_size = value
            if key == "memories_brand":
                self.memories_brand = value
