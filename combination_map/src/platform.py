from read_config import ReadConfig

class Platform:

    def __init__(self,fname):

        self.filename = fname
        config_file = ReadConfig(self.filename)
        dictionary = config_file.get_values()
        
        for key, value in dictionary.iteritems():
            if key == "kind":
                self.kind = value
            if key == "model":
                self.model = value
            if key == "no_soquets":
                self.no_soquets = value
            if key == "no_mem_dims":
                self.no_mem_dims = value
            if key == "no_sata_dims":
                self.no_sata_dims = value
            if key == "no_oculink_ports":
                self.no_oculink_ports = value
