class Device:
    def __init__(self, ip=None, rack=None, dc=None, u=None):
        self.ip = ip
        self.rack = rack
        self.dc = dc
        self.u = u

    def location(self):
        return "{}/{}/{}".format(self.dc, self.rack, self.u)

    def __repr__(self):
        return "{} ({})".format(self._type, self.location())

    def get_os(self):
        return None
