import hw
#import svc

services = [ 'http', 'ssh' ]
s = hw.Server(rack=1, u=2, dc=11, ip='192.168.1.1', services=services)
sw = hw.Switch(rack=1, dc=11, ip='192.168.2.2')

print(s)
print(sw)

print("Testing object types...")
for o in [ s, sw ]:
    print("{} is a device: {}".format(o, isinstance(o, hw.Device)))
    print("{} is a Switch: {}".format(o, isinstance(o, hw.Switch)))
    print("{} is a Server: {}".format(o, isinstance(o, hw.Server)))
