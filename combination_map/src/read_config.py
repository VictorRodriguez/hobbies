
class ReadConfig:
    d = {}
    def __init__(self,fname):
        with open(fname) as f:
                content = f.readlines()
        for line in content:
            key=line.split(":")[0].strip()
            value=line.split(":")[1].strip()
            self.d[key] = value

    def get_values(self):
        return self.d
