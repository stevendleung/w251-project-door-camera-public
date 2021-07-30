import cv2
import numpy as np
import paho.mqtt.client as mqtt
import sys
from datetime import datetime, timedelta
import os
import secrets

import argparse
import time
from pathlib import Path

noevent = ['image_3443.jpg']

events = [
['image_20.jpg', 'image_26.jpg', 'image_27.jpg', 'image_30.jpg', 'image_31.jpg'],
['image_23.jpg', 'image_32.jpg', 'image_33.jpg', 'image_40.jpg', 'image_49.jpg', 'image_54.jpg', 'image_56.jpg', 'image_62.jpg', 'image_67.jpg', 'image_74.jpg', 'image_76.jpg'],
['image_98.jpg', 'image_88.jpg', 'image_86.jpg', 'image_79.jpg', 'image_72.jpg', 'image_69.jpg', 'image_65.jpg', 'image_51.jpg'],
['image_161.jpg', 'image_157.jpg', 'image_153.jpg', 'image_148.jpg', 'image_147.jpg', 'image_146.jpg', 'image_141.jpg', 'image_138.jpg', 'image_133.jpg', 'image_119.jpg', 'image_180.jpg'],
['image_185.jpg', 'image_178.jpg', 'image_175.jpg', 'image_174.jpg', 'image_173.jpg'],
['image_251.jpg', 'image_248.jpg', 'image_247.jpg', 'image_242.jpg', 'image_239.jpg', 'image_238.jpg', 'image_236.jpg', 'image_233.jpg', 'image_232.jpg', 'image_275.jpg' ,'image_278.jpg'],
['image_335.jpg', 'image_329.jpg', 'image_319.jpg', 'image_315.jpg', 'image_311.jpg', 'image_308.jpg', 'image_300.jpg', 'image_298.jpg', 'image_293.jpg', 'image_288.jpg', 'image_286.jpg', 'image_283.jpg', 'image_281.jpg', 'image_268.jpg', 'image_259.jpg', 'image_340.jpg', 'image_343.jpg', 'image_357.jpg', 'image_410.jpg', 'image_400.jpg'],
['image_358.jpg', 'image_354.jpg', 'image_348.jpg', 'image_338.jpg', 'image_337.jpg'],
['image_631.jpg', 'image_627.jpg', 'image_622.jpg', 'image_612.jpg', 'image_605.jpg', 'image_603.jpg', 'image_598.jpg'],
['image_732.jpg', 'image_730.jpg', 'image_725.jpg', 'image_718.jpg', 'image_715.jpg', 'image_710.jpg', 'image_707.jpg', 'image_704.jpg', 'image_703.jpg', 'image_702.jpg', 'image_682.jpg', 'image_760.jpg', 'image_755.jpg', 'image_752.jpg', 'image_751.jpg', 'image_749.jpg', 'image_742.jpg'],
['image_445.jpg', 'image_442.jpg', 'image_438.jpg', 'image_564.jpg', 'image_563.jpg', 'image_551.jpg', 'image_548.jpg', 'image_508.jpg', 'image_507.jpg', 'image_494.jpg', 'image_596.jpg', 'image_589.jpg', 'image_583.jpg'],
['image_467.jpg', 'image_461.jpg'],
['image_780.jpg', 'image_781.jpg', 'image_782.jpg', 'image_805.jpg', 'image_800.jpg', 'image_797.jpg', 'image_795.jpg', 'image_793.jpg'],
['image_572.jpg', 'image_566.jpg'],
['image_640.jpg', 'image_644.jpg', 'image_733.jpg', 'image_734.jpg', 'image_787.jpg', 'image_789.jpg', 'image_840.jpg', 'image_837.jpg', 'image_849.jpg'],
['image_907.jpg', 'image_902.jpg', 'image_882.jpg', 'image_880.jpg'],
['image_966.jpg', 'image_960.jpg', 'image_959.jpg', 'image_954.jpg'],
['image_987.jpg', 'image_989.jpg', 'image_990.jpg', 'image_994.jpg'],
['image_1383.jpg', 'image_1381.jpg', 'image_1379.jpg', 'image_1378.jpg', 'image_1377.jpg', 'image_1376.jpg', 'image_1369.jpg', 'image_1367.jpg', 'image_1365.jpg', 'image_1364.jpg', 'image_1362.jpg', 'image_1355.jpg', 'image_1354.jpg', 'image_1342.jpg', 'image_1337.jpg', 'image_1335.jpg', 'image_1333.jpg', 'image_1332.jpg', 'image_1323.jpg', 'image_1319.jpg', 'image_1301.jpg', 'image_1296.jpg', 'image_1294.jpg', 'image_1286.jpg', 'image_1282.jpg', 'image_1281.jpg', 'image_1273.jpg', 'image_1265.jpg', 'image_1260.jpg', 'image_1255.jpg', 'image_1242.jpg', 'image_1232.jpg', 'image_1230.jpg', 'image_1229.jpg', 'image_1223.jpg', 'image_1221.jpg', 'image_1214.jpg', 'image_1206.jpg', 'image_1192.jpg', 'image_1191.jpg'],
['image_1144.jpg', 'image_1139.jpg', 'image_1072.jpg'],
['image_1160.jpg', 'image_1157.jpg', 'image_1156.jpg'],
['image_1187.jpg', 'image_1171.jpg'],
['image_1393.jpg', 'image_1392.jpg', 'image_1384.jpg'],
['image_1719.jpg', 'image_1718.jpg', 'image_1717.jpg', 'image_1705.jpg', 'image_1703.jpg', 'image_1699.jpg', 'image_1697.jpg'],
['image_1745.jpg', 'image_1740.jpg', 'image_1737.jpg', 'image_1732.jpg', 'image_1726.jpg'],
['image_2170.jpg', 'image_2167.jpg', 'image_2164.jpg', 'image_2158.jpg', 'image_2153.jpg', 'image_2151.jpg', 'image_2147.jpg', 'image_2145.jpg', 'image_2142.jpg', 'image_2134.jpg', 'image_2114.jpg', 'image_2111.jpg', 'image_2110.jpg', 'image_2108.jpg', 'image_2107.jpg', 'image_2099.jpg', 'image_2091.jpg', 'image_2089.jpg', 'image_2088.jpg', 'image_2086.jpg', 'image_2084.jpg', 'image_2081.jpg', 'image_2074.jpg', 'image_2070.jpg', 'image_2069.jpg', 'image_2062.jpg', 'image_2052.jpg', 'image_2048.jpg', 'image_2047.jpg', 'image_2034.jpg', 'image_2032.jpg', 'image_2031.jpg', 'image_2025.jpg', 'image_2016.jpg', 'image_2013.jpg', 'image_2005.jpg', 'image_2004.jpg', 'image_1999.jpg', 'image_1998.jpg', 'image_1995.jpg', 'image_1987.jpg', 'image_1986.jpg'],
['image_2342.jpg', 'image_2339.jpg', 'image_2334.jpg', 'image_2326.jpg', 'image_2322.jpg', 'image_2317.jpg', 'image_2314.jpg'],
['image_2306.jpg', 'image_2269.jpg', 'image_2267.jpg', 'image_2261.jpg'],
['image_1652.jpg', 'image_1649.jpg', 'image_1648.jpg'],
['image_1474.jpg', 'image_1489.jpg'],
['image_1514.jpg', 'image_1515.jpg'],
['image_1886.jpg', 'image_1851.jpg'],
['image_1914.jpg', 'image_1915.jpg', 'image_1918.jpg', 'image_1928.jpg', 'image_1929.jpg'],
['image_1950.jpg', 'image_1958.jpg', 'image_1962.jpg', 'image_1972.jpg'],
['image_2199.jpg', 'image_2192.jpg', 'image_2183.jpg', 'image_2174.jpg'], 
['image_2358.jpg', 'image_2357.jpg', 'image_2356.jpg'],
['image_2605.jpg', 'image_2602.jpg', 'image_2593.jpg', 'image_2581.jpg', 'image_2579.jpg', 'image_2570.jpg', 'image_2568.jpg', 'image_2564.jpg', 'image_2554.jpg', 'image_2541.jpg', 'image_2537.jpg', 'image_2530.jpg', 'image_2527.jpg'],
['image_2753.jpg', 'image_2755.jpg', 'image_2761.jpg', 'image_2769.jpg', 'image_2770.jpg', 'image_2771.jpg', 'image_2774.jpg', 'image_2776.jpg'],
['image_4413.jpg', 'image_4414.jpg', 'image_4418.jpg', 'image_4420.jpg', 'image_4421.jpg', 'image_4424.jpg', 'image_4425.jpg'],
['image_4317.jpg', 'image_4320.jpg', 'image_4327.jpg', 'image_4332.jpg', 'image_4333.jpg', 'image_4339.jpg', 'image_4348.jpg', 'image_4370.jpg', 'image_4371.jpg', 'image_4378.jpg', 'image_4384.jpg', 'image_4385.jpg', 'image_4391.jpg', 'image_4397.jpg', 'image_4399.jpg'],
['image_4373.jpg', 'image_4375.jpg', 'image_4383.jpg', 'image_4389.jpg'],
['image_2383.jpg', 'image_2379.jpg', 'image_2374.jpg', 'image_2364.jpg'],
['image_2440.jpg', 'image_2438.jpg', 'image_2433.jpg', 'image_2427.jpg', 'image_2421.jpg'],
['image_2686.jpg', 'image_2674.jpg', 'image_2671.jpg', 'image_2666.jpg', 'image_2664.jpg'], 
['image_2712.jpg', 'image_2697.jpg', 'image_2692.jpg'],
['image_2729.jpg', 'image_2731.jpg', 'image_2732.jpg'], 
['image_2446.jpg', 'image_2445.jpg'],
['image_2460.jpg', 'image_2461.jpg'], 
['image_2489.jpg', 'image_2488.jpg', 'image_2472.jpg'],
['image_2452.jpg'],
['image_2510.jpg', 'image_2505.jpg'],
['image_2797.jpg', 'image_2789.jpg', 'image_2788.jpg', 'image_2784.jpg'],
['image_2826.jpg', 'image_2816.jpg', 'image_2815.jpg', 'image_2813.jpg', 'image_2804.jpg'],
['image_2852.jpg', 'image_2840.jpg', 'image_2839.jpg', 'image_2832.jpg', 'image_2831.jpg'], 
['image_2878.jpg', 'image_2870.jpg', 'image_2863.jpg'],
['image_2881.jpg', 'image_2889.jpg', 'image_2891.jpg'], 
['image_2919.jpg', 'image_2911.jpg', 'image_2909.jpg', 'image_2905.jpg'],
['image_2930.jpg', 'image_2929.jpg'],
['image_4434.jpg', 'image_4436.jpg'],
['image_4453.jpg', 'image_4455.jpg'],
['image_4280.jpg', 'image_4283.jpg', 'image_4284.jpg', 'image_4289.jpg', 'image_4293.jpg', 'image_4305.jpg', 'image_4306.jpg', 'image_4309.jpg', 'image_4310.jpg'],
['image_4219.jpg', 'image_4223.jpg', 'image_4226.jpg', 'image_4229.jpg', 'image_4230.jpg', 'image_4231.jpg', 'image_4242.jpg', 'image_4245.jpg', 'image_4247.jpg', 'image_4248.jpg', 'image_4252.jpg', 'image_4255.jpg', 'image_4262.jpg', 'image_4264.jpg'],
['image_4112.jpg', 'image_4129.jpg', 'image_4131.jpg', 'image_4135.jpg', 'image_4139.jpg', 'image_4140.jpg'],
['image_4044.jpg', 'image_4050.jpg', 'image_4059.jpg', 'image_4062.jpg', 'image_4076.jpg', 'image_4078.jpg', 'image_4080.jpg', 'image_4085.jpg', 'image_4086.jpg', 'image_4087.jpg', 'image_4088.jpg', 'image_4089.jpg', 'image_4099.jpg', 'image_4101.jpg', 'image_4104.jpg', 'image_4109.jpg'],
['image_3601.jpg', 'image_3603.jpg'],
['image_3009.jpg', 'image_3000.jpg', 'image_2996.jpg', 'image_2991.jpg', 'image_2980.jpg', 'image_2978.jpg'],
['image_3056.jpg', 'image_3014.jpg'],
['image_3452.jpg', 'image_3451.jpg', 'image_3450.jpg', 'image_3443.jpg', 'image_3439.jpg'],
['image_3487.jpg', 'image_3480.jpg', 'image_3479.jpg', 'image_3467.jpg', 'image_3465.jpg', 'image_3462.jpg'],
['image_3575.jpg', 'image_3566.jpg', 'image_3562.jpg', 'image_3556.jpg', 'image_3552.jpg', 'image_3548.jpg'],
['image_3649.jpg', 'image_3637.jpg', 'image_3634.jpg', 'image_3631.jpg', 'image_3620.jpg'],
['image_3700.jpg', 'image_3696.jpg', 'image_3695.jpg', 'image_3694.jpg', 'image_3692.jpg', 'image_3689.jpg', 'image_3686.jpg', 'image_3674.jpg'],
['image_3820.jpg', 'image_3826.jpg', 'image_3830.jpg', 'image_3837.jpg'],
['image_3849.jpg', 'image_3857.jpg', 'image_3864.jpg', 'image_3866.jpg', 'image_3880.jpg', 'image_3881.jpg'],
['image_3929.jpg', 'image_3925.jpg', 'image_3923.jpg', 'image_3922.jpg', 'image_3921.jpg', 'image_3920.jpg', 'image_3919.jpg', 'image_3912.jpg', 'image_3908.jpg', 'image_3901.jpg', 'image_3899.jpg'],
['image_3983.jpg', 'image_3981.jpg', 'image_3974.jpg', 'image_3969.jpg', 'image_3968.jpg', 'image_3962.jpg'],
['image_4003.jpg', 'image_4000.jpg', 'image_3997.jpg', 'image_3993.jpg', 'image_3989.jpg'],
['image_4023.jpg', 'image_4021.jpg', 'image_4015.jpg', 'image_4012.jpg']
]

# Mosquitto 
# LOCAL_MQTT_HOST= "mosquitto-service"
LOCAL_MQTT_HOST= "localhost"
LOCAL_MQTT_PORT= 1883
LOCAL_IMAGE_TOPIC= "image_topic"
#LOCAL_NOTIF_TOPIC= "model_output_topic"
PUBLISH_TOPIC = LOCAL_IMAGE_TOPIC

local_mqttclient = mqtt.Client()

# Define Local Sender MQTT callbacks
def on_connect_local(client, userdata, flags, rc):
  print("connected to ", PUBLISH_TOPIC, " with rc: " + str(rc))

def on_disconnect_local(client, userdata, flags, rc): 
  print("Disconnected from local broker, result code" + str(rc))
  local_sender_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_publish_local(client, userdata, msg_id):
    print("Message successfully published: {}".format(msg_id))

# Make connections to local broker
local_mqttclient.on_connect = on_connect_local
local_mqttclient.on_publish = on_publish_local
local_mqttclient.on_disconnect = on_disconnect_local
vid_source = 1

# Publishing message to the Notification Queue as an output from the model
# Message Structure:
#   Video Source Id: 1 (default)
#   Type of Report: 0 (FaceRec); 1 (Del[ivery]Nodel[ivery])
#   Classification: 
#       If Type of Report = 0 (FaceRec)
#           0 (Known Person)
#           1 (Unknown Person)
#       If Type of Report = 1 (DelNodel)
#           0 (Delivery)
#           1 (Non-Delivery)
#   Person Name: string
#   Filename: string
#   Box Coordinates: x, y, w, h 
#   
#   Example: 1; 0; 0; Steven; image_380.jpg; 0.234,0.123,0.346,0.778
#   Example: 1; 1; 0; ; image_480.jpg; 0.234,0.123,0.346,0.778

def publishDataToModel(topicName):
    try:
        path = "/home/data"
        # publish all events to the queue
        for event in events:
            for ndx in range(len(event)):
                filename=event[ndx]
                mesg = "{};{};{}".format(vid_source, path, filename)
                local_mqttclient.publish(topicName, mesg)
                # messages are written once every second; sleep for 80th percent of time
                time.sleep(0.8)
            
            # after every event, wait for a random amount of time (5 seconds for testing)
            random_sleep_time = secrets.randbelow(5)
            time.sleep(random_sleep_time)
    except:
      print("Unexpected error:", sys.exc_info()[0])

def run():
    # connect to the MQTT HOST
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
    publishDataToModel(LOCAL_IMAGE_TOPIC)

def main():
    run()

if __name__ == "__main__":
    main()
