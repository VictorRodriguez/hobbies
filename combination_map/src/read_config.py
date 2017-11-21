class ReadConfig:
    sim_dic = {}
    db_array = []

    def __init__(self,fname):
        self.fname = fname
        

    def load_simulation_values(self):
        with open(self.fname) as f:
                content = f.readlines()
        for line in content:
            if line.startswith('#') or line.startswith("//"):
                pass
            elif ":" in line:
                key=line.split(":")[0].strip()
                value=line.split(":")[1].strip()
                self.sim_dic[key] = value

    def load_db_values(self):
        array_fields = []
        self.db_array = []
        with open(self.fname) as f:
                content = f.readlines()
        for line in content:
            tmp_dic = {}
            array_values = []
            if line.startswith('#') or line.startswith("//"):
                pass
            elif "ID" in line:
                array_fields = filter(None,line.strip().split(","))
            else:
                array_values = filter(None,line.strip().split(","))
                if len(array_fields) and len(array_values):
                    if len(array_values) == len(array_fields):
                        tmp_dic = dict(zip(array_fields, array_values))
                    else:
                        print("ERROR: in %s arrays != size" % self.fname)
                        print("ERROR: in line: %s" % line.strip())
                        print("ERROR: len(array_fields) = %s" % len(array_fields))
                        print("ERROR: len(array_values) = %s" % len(array_values))
                else:
                    print("ERROR: in % array = 0" % self.fname)
                    print("ERROR: in line: %s" % line.strip())
                    print("ERROR: len(array_fields) = %s" % len(array_fields))
                    print("ERROR: len(array_values) = %s" % len(array_values))
            self.db_array.append(tmp_dic)
        self.db_array = filter(None,self.db_array)

    def get_comp_items(self):
        return self.db_array

    def get_sim_files(self):
        return self.sim_dic
