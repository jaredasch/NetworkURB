import random
import time
import math
import matplotlib.pyplot as plt
import Entity

import warnings

warnings.filterwarnings("ignore",".*GUI is implemented.*")

# define iot
IOT_TYPE = "x-scale","fog-scale","cloud-sacle";
IOTs_number = 50;
IOT_NUMBER_X_SCALE =  int (IOTs_number / 2);
IOT_NUMBER_FOG_SCALE = int ( ( IOTs_number -  IOT_NUMBER_X_SCALE ) * 2 / 3 );
IOT_NUMBER_CLOUD_SCALE = IOTs_number - IOT_NUMBER_X_SCALE - IOT_NUMBER_FOG_SCALE;

# define simulation area matrix
SIMULATION_AREA_WIDTH_X = 50 * 30;
SIMULATION_AREA_WIDTH_Y = 50 * 30;


# create access point, create IOTs
APs = []
APs_number = 3;
APs.append(Entity.Device(750,300,"AP","AP"+"-#1"));
APs.append(Entity.Device(300,1200,"AP","AP"+"-#2"));
APs.append(Entity.Device(1200,1200,"AP","AP"+"-#3"));

IOTs = []
for i in range(IOT_NUMBER_X_SCALE):
    type = "x-scale"
    IOTs.append(Entity.Device(random.randint(3, int(SIMULATION_AREA_WIDTH_X/30))*30,random.randint(3, int(SIMULATION_AREA_WIDTH_X/30))*30,type, type+ "-#"+str(i)))
for i in range(IOT_NUMBER_FOG_SCALE):
    type = "fog-scale"
    IOTs.append(Entity.Device(random.randint(3, int(SIMULATION_AREA_WIDTH_X/30))*30,random.randint(3, int(SIMULATION_AREA_WIDTH_X/30))*30,type, type+ "-#"+str(i)))
for i in range(IOT_NUMBER_CLOUD_SCALE):
    type = "cloud-scale"
    IOTs.append(Entity.Device(random.randint(3, int(SIMULATION_AREA_WIDTH_X/30))*30,random.randint(3, int(SIMULATION_AREA_WIDTH_X/30))*30,type, type+ "-#"+str(i)))

# create LocalSDNs
LocalSDNs = []
LocalSDNs_X = [750,500,1000]
LocalSDNs_Y = [500,1000,1000]
LocalSDNs_number = 3;
LocalSDNs.append(Entity.Device(LocalSDNs_X[0], LocalSDNs_Y[0], "LocalSDN", "LocalSDN-#1"));
LocalSDNs.append(Entity.Device(LocalSDNs_X[1], LocalSDNs_Y[1], "LocalSDN", "LocalSDN-#2"));
LocalSDNs.append(Entity.Device(LocalSDNs_X[2], LocalSDNs_Y[2], "LocalSDN", "LocalSDN-#3"));
# view

# draw IoTs
def IoTsDraw():
    IOTx_X_SCALE = []
    IOTy_X_SCALE = []
    IOTcolors_X_SCALE = []

    IOTx_FOG_SCALE = []
    IOTy_FOG_SCALE = []
    IOTcolors_FOG_SCALE = []

    IOTx_CLOUD_SCALE = []
    IOTy_CLOUD_SCALE = []
    IOTcolors_CLOUD_SCALE = []

    for i in range(IOTs_number):
        if IOTs[i].type == "x-scale" :
            IOTx_X_SCALE.append(IOTs[i].x);
            IOTy_X_SCALE.append(IOTs[i].y);
            IOTcolors_X_SCALE.append("y")
        if IOTs[i].type == "fog-scale" :
            IOTx_FOG_SCALE.append(IOTs[i].x);
            IOTy_FOG_SCALE.append(IOTs[i].y);
            IOTcolors_FOG_SCALE.append("m")
        if IOTs[i].type == "cloud-scale" :
            IOTx_CLOUD_SCALE.append(IOTs[i].x);
            IOTy_CLOUD_SCALE.append(IOTs[i].y);
            IOTcolors_CLOUD_SCALE.append("c")
    plt.scatter(IOTx_X_SCALE, IOTy_X_SCALE, marker='o', s=8100 , alpha=0.2, c=IOTcolors_X_SCALE);
    plt.scatter(IOTx_X_SCALE, IOTy_X_SCALE, c=IOTcolors_X_SCALE, label="IOT_X_SCALE");
    plt.scatter(IOTx_FOG_SCALE, IOTy_FOG_SCALE, c=IOTcolors_FOG_SCALE, label="IOT_FOG_SCALE");
    plt.scatter(IOTx_CLOUD_SCALE, IOTy_CLOUD_SCALE, c=IOTcolors_CLOUD_SCALE, label="IOT_CLOUD_SCALE");

# draw Connectivity Requirement

# IoT with AP
def IoT_Connect_AP():
    for i in range(IOTs_number):
        min_distance = [0, SIMULATION_AREA_WIDTH_X];
        for j in range(APs_number):
            distance = math.sqrt(pow((APs[j].x - IOTs[i].x),2)+pow((APs[j].y - IOTs[i].y),2))
            if distance < min_distance[1]:
                min_distance[0] = j;
                min_distance[1] = distance;
        if min_distance[1] <= 1000:
                plt.plot([IOTs[i].x,APs[min_distance[0]].x],[IOTs[i].y,APs[min_distance[0]].y], '--',color="#800080",linewidth=0.5);
                APs[min_distance[0]].IoTs.append(IOTs[i]);
    for i in range(APs_number):
        string = APs[i].id +" ,location: ["+ str(APs[i].x)+","+ str(APs[i].y)+"] ,connectivity reqirement: [";
        for IOT in APs[i].IoTs:
            string = string + IOT.id + ",";
            #if IOT.type == "x-scale":
                #for xIot in APs[i].IoTs:
                    #if xIot.type == "x-scale":
                        #plt.plot([IOT.x, xIot.x], [IOT.y, xIot.y],"--",color="#006600", linewidth=0.2);
        string = string +"]";
        print(string)

# LocalSDN with AP
def LocalSDN_Connect_AP():
    LocalSDN_With_AP_X = [];
    LocalSDN_With_AP_Y = [];
    for i in range(APs_number):
        min_distance = [0, SIMULATION_AREA_WIDTH_X];
        for j in range(LocalSDNs_number):
            distance = math.sqrt(pow((APs[i].x - LocalSDNs[j].x), 2) + pow((APs[i].y - LocalSDNs[j].y), 2))
            if distance < min_distance[1]:
                min_distance[0] = j;
                min_distance[1] = distance;
        plt.plot([LocalSDNs[min_distance[0]].x, APs[i].x], [LocalSDNs[min_distance[0]].y, APs[i].y], 'b-', linewidth=0.5);
        LocalSDNs[min_distance[0]].APs.append(APs[i]);


# draw Central_SDN
Central_SDN = Entity.Device(750,750,"CentralSDN","CentralSDN0")
def Central_SDNDraw():
    Central_SDNcolors = ["g"]
    plt.scatter([Central_SDN.x], [Central_SDN.y], c=Central_SDNcolors, label="Central_SDN");


# LocalSDN with Central_SDN
def Central_SDN_Connect_Local_SDN():
    for i in range(LocalSDNs_number):
        plt.plot([LocalSDNs[i].x, Central_SDN.x], [LocalSDNs[i].y, Central_SDN.y], 'b-',linewidth=0.5);
        Central_SDN.localSDNs.append(LocalSDNs[i]);

# draw LocalSDNs
def LocalSDNsDraw():
    LocalSDNsx = []
    LocalSDNsy = []
    LocalSDNscolors = []
    for i in range(LocalSDNs_number):
        LocalSDNsx.append(LocalSDNs[i].x);
        LocalSDNsy.append(LocalSDNs[i].y);
        LocalSDNscolors.append("g");
    plt.scatter(LocalSDNsx, LocalSDNsy, c=LocalSDNscolors,marker='^',label="LocalSDNs");

# draw APs
def APsDraw():
    APx = []
    APy = []
    APcolors = []
    for i in range(APs_number):
        APx.append(APs[i].x);
        APy.append(APs[i].y);
        APcolors.append("r");
    plt.scatter(APx, APy, c=APcolors,label="AP");

# AP movement
def APMove():
    for i in range(APs_number):
        x = APs[i].x + random.randint(-Entity.RED_CAR_SPEED,Entity.RED_CAR_SPEED);
        y = APs[i].y + random.randint(-Entity.RED_CAR_SPEED, Entity.RED_CAR_SPEED);
        if x >= 0 and x <= 1000:
            APs[i].x = x;
        if y >= 0 and y <= 1000:
            APs[i].y = y;

# Local_SDN allocate channel to IoTs
def Local_SDN_allocate_channel():
    for SDN in LocalSDNs:
        x_Number = 0;
        fog_Number = 0;
        cloud_Number = 0;
        for AP in SDN.APs:
            for IOT in AP.IoTs:
                if IOT.type == "x-scale":
                    IOT.channel = SDN.x_spectrum[x_Number];
                    x_Number = x_Number + 1;
                    plt.plot([SDN.x, IOT.x], [SDN.y, IOT.y], '-',color='darkgreen', linewidth=0.2);
                if IOT.type == "fog-scale":
                    IOT.channel = SDN.fog_spectrum[fog_Number];
                    fog_Number = fog_Number + 1;
                    plt.plot([SDN.x, IOT.x], [SDN.y, IOT.y], '-',color='darkgreen', linewidth=0.2);
                if IOT.type == "Laptop":
                    IOT.channel = SDN.Laptop_spectrum[L_Number];
                    L_Number = L_Number + 1;
                    plt.plot([SDN.x, IOT.x], [SDN.y, IOT.y], '-',color='darkgreen', linewidth=0.2);
    for i in range(IOTs_number):
        if IOTs[i].type ==  "Google Glass":
            print(IOTs[i]);
    for i in range(IOTs_number):
        if IOTs[i].type ==  "Mobile":
            print(IOTs[i]);
    for i in range(IOTs_number):
        if IOTs[i].type ==  "Laptop":
            print(IOTs[i]);

def Fog():
    for i in range(APs_number):
        if i != APs_number-1:
            plt.plot([APs[i].x, APs[i+1].x], [APs[i].y, APs[i+1].y], '-', color='magenta', linewidth=0.8);
        else:
            plt.plot([APs[i].x, APs[0].x], [APs[i].y, APs[0].y], '-', color='magenta', linewidth=0.8);


# light speed
c = 2.4 * (10**8);
bandwidth = 10**6 ;
request_size = 1000 * 8;
reply_size = 2000 * 8;
wait_time = 0.1 ;

def calculate_x(SDN,AP,IOT):
    # IOT - AP - SDN - calculate - AP - IOT
    distance_iot_ap = math.sqrt( (IOT.x - AP.x)**2 + (IOT.y - AP.y)**2 );
    distance_ap_sdn = math.sqrt( (SDN.x - AP.x)**2 + (SDN.y - AP.y)**2 );

    time_iot_ap_request = request_size / bandwidth + distance_iot_ap / c ;
    time_ap_sdn_request = request_size / bandwidth + distance_ap_sdn / c;

    time_iot_ap_reply = reply_size / bandwidth + distance_iot_ap / c;
    time_ap_sdn_reply = reply_size / bandwidth + distance_ap_sdn / c;

    return time_iot_ap_request+time_ap_sdn_request+wait_time+time_iot_ap_reply+time_ap_sdn_reply;

def calculate_fog(SDN,AP,IOT):
    # IOT - AP - SDN - calculate - AP - IOT
    distance_iot_ap = math.sqrt( (IOT.x - AP.x)**2 + (IOT.y - AP.y)**2 );
    distance_ap_sdn = math.sqrt( (SDN.x - AP.x)**2 + (SDN.y - AP.y)**2 );

    time_iot_ap_request = request_size / (bandwidth*2) + distance_iot_ap / c ;
    time_ap_sdn_request = request_size / (bandwidth*2) + distance_ap_sdn / c;

    time_iot_ap_reply = reply_size / (bandwidth*2) + distance_iot_ap / c;
    time_ap_sdn_reply = reply_size / (bandwidth*2) + distance_ap_sdn / c;

    return time_iot_ap_request+time_ap_sdn_request+wait_time+time_iot_ap_reply+time_ap_sdn_reply;

def calculate_cloud(SDN,AP,IOT):
    # IOT - AP - SDN - Centrol SDN - calculate - SDN - AP - IOT
    distance_iot_ap = math.sqrt( (IOT.x - AP.x)**2 + (IOT.y - AP.y)**2 );
    distance_ap_sdn = math.sqrt( (SDN.x - AP.x)**2 + (SDN.y - AP.y)**2 );
    distance_sdn_central = math.sqrt((SDN.x - Central_SDN.x) ** 2 + (SDN.y - Central_SDN.y) ** 2);

    time_iot_ap_request = request_size / (bandwidth*3) + distance_iot_ap / c ;
    time_ap_sdn_request = request_size / (bandwidth*3) + distance_ap_sdn / c;
    time_sdn_central_request = request_size / (bandwidth * 3) + distance_sdn_central / c;

    time_iot_ap_reply = reply_size / (bandwidth*3) + distance_iot_ap / c;
    time_ap_sdn_reply = reply_size / (bandwidth*3) + distance_ap_sdn / c;
    time_sdn_central_reply = reply_size / (bandwidth * 3) + distance_ap_sdn / c;

    return time_iot_ap_request+time_ap_sdn_request+time_sdn_central_request+wait_time+time_sdn_central_reply+time_iot_ap_reply+time_ap_sdn_reply;

def scale_communication_x():
    data_time_x = [];
    data_time_fog = [];
    data_time_cloud = [];
    for SDN in LocalSDNs:
        for AP in APs:
            for IOT in AP.IoTs:
                if IOT.type == "x-scale":
                    data_time_x.append(calculate_x(SDN,AP,IOT));
                if IOT.type == "fog-scale":
                    data_time_fog.append(calculate_fog(SDN,AP,IOT));
                if IOT.type == "cloud-scale":
                    data_time_cloud.append(calculate_cloud(SDN,AP,IOT));
    print(data_time_x)
    print(data_time_fog)
    print(data_time_cloud)

fig = plt.gcf()
#fig.set_size_inches(16.5, 6.5)

plt.axis([0, SIMULATION_AREA_WIDTH_X , 0, SIMULATION_AREA_WIDTH_Y ])
plt.ylabel('simulation area Y (m)')
plt.xlabel('simulation area X (m)')




IoTsDraw();
plt.pause(0.5);
APsDraw();
plt.pause(0.5);
IoT_Connect_AP();
plt.pause(0.5);
LocalSDNsDraw();
plt.pause(0.5);
LocalSDN_Connect_AP();
plt.pause(0.5);
Central_SDNDraw();
plt.pause(0.5);
Central_SDN_Connect_Local_SDN();
#Central_SDN.allocate_spectrum();
#Local_SDN_allocate_channel();
scale_communication_x();

Fog();
plt.legend(loc="upper right");
plt.show();



