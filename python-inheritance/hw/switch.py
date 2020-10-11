from hw.device import Device

class Switch(Device):
    _type = 'Switch'

    def __init__(self, ports=24, top=True, **kwargs):
        self.ports = ports
        self.top = True
        if kwargs.get('u', None) is None and top:
            kwargs['u'] = 42
        super().__init__(**kwargs)
