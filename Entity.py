RED_CAR_SPEED = 50;
GREEN_CAR_SPEED = 0;
IOT_SPEED = 5;

# spectrum reserved for google devices requirement from channel 0 - 19
# spectrum reserved for mobile devices requirement from channel 20 - 39
# spectrum reserved for google devices requirement from channel 40 - 59
# spectrum reserved for cloud devices requirement from channel 60 - 100


Spectrum = list(range(50))


class Unit:
    def __init__(self, x, y, type):
        self.x = x;
        self.y = y;
        self.type = type;
        if self.type == "AP":
            self.speed = RED_CAR_SPEED;
            self.IoTs = [];
            self.CRC = [];
        elif self.type == "LocalSDN":
            self.speed = GREEN_CAR_SPEED;
            self.APs = []
            self.x_spectrum = [];
            self.fog_spectrum = [];
            self.cloud_spectrum = [];
        elif self.type == "CentralSDN":
            self.speed = GREEN_CAR_SPEED;
            self.localSDNs = [];
            self.x_spectrum = [];
            self.fog_spectrum = [];
            self.cloud_spectrum = [];
        else:
            self.speed = IOT_SPEED;
            self.channel = None;

    def allocate_channel(self, IOT, channel):
        IOT.channel = channel;

    def allocate_spectrum(self):
        Number = 0;
        for SDN in self.localSDNs:
            for AP in SDN.APs:
                for IOT in AP.IoTs:
                    if IOT.type == "x-scale":
                        SDN.x_spectrum.append(Spectrum[Number]);
                        Number = Number + 1;
                    if IOT.type == "fog-scale":
                        SDN.fog_spectrum.append(Spectrum[Number]);
                        SDN.fog_spectrum.append(Spectrum[Number + 1]);
                        Number = Number + 2;
                    if IOT.type == "cloud-scale":
                        SDN.cloud_spectrum.append(Spectrum[Number]);
                        SDN.cloud_spectrum.append(Spectrum[Number + 1]);
                        SDN.cloud_spectrum.append(Spectrum[Number + 2]);
                        Number = Number + 3;
            print(SDN.id + ",spectrum for x-scale" + str(SDN.x_spectrum) + ",spectrum for fog" + str(SDN.fog_spectrum) + ",spectrum for cloud" + str(SDN.cloud_spectrum));
            string = SDN.id + ", control ["
            for AP in SDN.APs:
                string = string + AP.id + ","
            string = string + "]"
            print(string)


class Device(Unit):
    def __init__(self, x, y, type, id):
        Unit.__init__(self, x, y, type);
        self.id = id;

    def __str__(self):
        if self.type != "AP" and self.type != "LocalSDN" and self.type != "CentralSDN":
            return "Device : [" + self.type + ",location:(" + str(self.x) + "," + str(self.y) + ")" + ",speed:" + str(self.speed) + ",id:" + self.id + ",channel:" + str(self.channel) + "]"
        else:
            return "[" + self.type + ",location:(" + str(self.x) + "," + str(self.y) + ")" + ",speed:" + str(self.speed) + ",id:" + self.id + "]"


class CR:
    def __init__(self, id, requirement):
        self.id = id;
        self.requirement = requirement;

