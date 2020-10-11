from hw.device import Device

class Server(Device):
    _type = 'Server'

    def __init__(self, services=None, **kwargs):
        self.services = services
        super().__init__(**kwargs)
