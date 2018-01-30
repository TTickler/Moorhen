from Shipper import *
class HardwareMetricShipper(Shipper):
    def __init__(self):

        #initialization of software type shipper
        Shipper.__init__("software")