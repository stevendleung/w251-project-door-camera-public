import cv2
import numpy as np
import paho.mqtt.client as mqtt
import sys
from datetime import datetime, timedelta
import os
import random

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

events = [
['image_3619000001.jpg'],
['image_1663000001.jpg', 'image_1661000001.jpg'],
['image_2421000000.jpg', 'image_2427000000.jpg', 'image_2428000000.jpg', 'image_2425000000.jpg'],
['image_3554000000.jpg', 'image_3557000000.jpg', 'image_3549000000.jpg'],
['image_1656000001.jpg', 'image_1655000001.jpg'],
['image_2373000001.jpg', 'image_2383000001.jpg', 'image_2372000001.jpg', 'image_2366000001.jpg', 'image_2385000001.jpg', 'image_2391000001.jpg', 'image_2388000001.jpg', 'image_2368000001.jpg', 'image_2371000001.jpg', 'image_2392000001.jpg', 'image_2364000001.jpg', 'image_2393000001.jpg'],
['image_1736000001.jpg', 'image_1731000001.jpg', 'image_1734000001.jpg', 'image_1733000001.jpg', 'image_1742000001.jpg'],
['image_2623000000.jpg', 'image_2652000000.jpg', 'image_2609000000.jpg', 'image_2631000000.jpg', 'image_2658000000.jpg', 'image_2647000000.jpg', 'image_2653000000.jpg', 'image_2666000000.jpg', 'image_2638000000.jpg', 'image_2650000000.jpg', 'image_2606000000.jpg', 'image_2627000000.jpg', 'image_2639000000.jpg', 'image_2657000000.jpg', 'image_2634000000.jpg', 'image_2651000000.jpg'],
['image_1585000000.jpg'],
['image_1752000001.jpg', 'image_1754000001.jpg', 'image_1763000001.jpg'],
['image_2574000000.jpg', 'image_2575000000.jpg'],
['image_1649000000.jpg'],
['image_4299000000.jpg', 'image_4289000000.jpg'],
['image_4022000001.jpg', 'image_4010000001.jpg', 'image_4018000001.jpg', 'image_4019000001.jpg'],
['image_3862000001.jpg', 'image_3853000001.jpg', 'image_3854000001.jpg'],
['image_4053000001.jpg', 'image_4088000001.jpg', 'image_4107000001.jpg', 'image_4060000001.jpg', 'image_4067000001.jpg', 'image_4052000001.jpg', 'image_4096000001.jpg', 'image_4106000001.jpg', 'image_4061000001.jpg', 'image_4070000001.jpg', 'image_4062000001.jpg', 'image_4076000001.jpg', 'image_4102000001.jpg', 'image_4071000001.jpg', 'image_4065000001.jpg', 'image_4104000001.jpg'],
['image_1123000000.jpg', 'image_1102000000.jpg', 'image_1111000000.jpg', 'image_1098000000.jpg', 'image_1119000000.jpg', 'image_1096000000.jpg', 'image_1126000000.jpg', 'image_1107000000.jpg', 'image_1139000000.jpg'],
['image_4270000000.jpg', 'image_4281000000.jpg', 'image_4276000000.jpg', 'image_4246000000.jpg', 'image_4252000000.jpg', 'image_4254000000.jpg'],
['image_5041000000.jpg', 'image_5066000000.jpg', 'image_5050000000.jpg'],
['image_1203000000.jpg', 'image_1183000000.jpg', 'image_1185000000.jpg', 'image_1201000000.jpg', 'image_1200000000.jpg'],
['image_5124000000.jpg', 'image_5123000000.jpg'],
['image_4089000000.jpg', 'image_4080000000.jpg'],
['image_2554000000.jpg', 'image_2569000000.jpg', 'image_2564000000.jpg', 'image_2562000000.jpg', 'image_2549000000.jpg'],
['image_1778000001.jpg', 'image_1775000001.jpg', 'image_1776000001.jpg'],
['image_1646000001.jpg'],
['image_2637000001.jpg', 'image_2631000001.jpg', 'image_2622000001.jpg', 'image_2633000001.jpg'],
['image_1569000000.jpg'],
['image_1655000000.jpg'],
['image_3561000000.jpg', 'image_3562000000.jpg'],
['image_1747000000.jpg', 'image_1755000000.jpg', 'image_1759000000.jpg', 'image_1749000000.jpg'],
['image_2414000000.jpg', 'image_2403000000.jpg'],
['image_3611000000.jpg', 'image_3603000000.jpg', 'image_3599000000.jpg'],
['image_2439000001.jpg', 'image_2434000001.jpg', 'image_2419000001.jpg', 'image_2436000001.jpg', 'image_2431000001.jpg'],
['image_1779000000.jpg', 'image_1774000000.jpg', 'image_1681000000.jpg', 'image_1665000000.jpg', 'image_1776000000.jpg', 'image_1675000000.jpg', 'image_1684000000.jpg', 'image_1659000000.jpg'],
['image_1189000001.jpg', 'image_1180000001.jpg'],
['image_4116000000.jpg', 'image_4125000000.jpg'],
['image_5115000000.jpg', 'image_5097000000.jpg', 'image_5095000000.jpg', 'image_5092000000.jpg'],
['image_1146000001.jpg', 'image_1140000001.jpg', 'image_1111000001.jpg', 'image_1112000001.jpg', 'image_1144000001.jpg', 'image_1107000001.jpg', 'image_1148000001.jpg', 'image_1145000001.jpg', 'image_1072000001.jpg', 'image_1139000001.jpg'],
['image_4024000000.jpg'],
['image_5085000000.jpg', 'image_5083000000.jpg', 'image_5090000000.jpg', 'image_5084000000.jpg', 'image_5073000000.jpg', 'image_5082000000.jpg', 'image_5076000000.jpg', 'image_5077000000.jpg'],
['image_4302000001.jpg', 'image_4310000001.jpg', 'image_4304000001.jpg', 'image_4292000001.jpg', 'image_4298000001.jpg', 'image_4305000001.jpg', 'image_4275000001.jpg', 'image_4301000001.jpg', 'image_4288000001.jpg'],
['image_3929000001.jpg', 'image_3917000001.jpg', 'image_3910000001.jpg', 'image_3902000001.jpg', 'image_3890000001.jpg'],
['image_4311000000.jpg', 'image_4313000000.jpg'],
['image_3996000001.jpg', 'image_4001000001.jpg'],
['image_1360000000.jpg'],
['image_5175000000.jpg'],
['image_5385000001.jpg', 'image_5388000001.jpg'],
['image_5336000001.jpg', 'image_5322000001.jpg', 'image_5327000001.jpg', 'image_5333000001.jpg', 'image_5332000001.jpg', 'image_5320000001.jpg', 'image_5318000001.jpg', 'image_5343000001.jpg'],
['image_1026000001.jpg'],
['image_4418000001.jpg', 'image_4419000001.jpg', 'image_4414000001.jpg', 'image_4424000001.jpg', 'image_4410000001.jpg', 'image_4416000001.jpg', 'image_4423000001.jpg'],
['image_4610000000.jpg', 'image_4820000000.jpg', 'image_4768000000.jpg', 'image_4661000000.jpg', 'image_4659000000.jpg', 'image_4616000000.jpg', 'image_4602000000.jpg', 'image_4813000000.jpg', 'image_4672000000.jpg', 'image_4715000000.jpg', 'image_4800000000.jpg', 'image_4776000000.jpg', 'image_4683000000.jpg', 'image_4718000000.jpg', 'image_4688000000.jpg', 'image_4707000000.jpg', 'image_4713000000.jpg', 'image_4636000000.jpg', 'image_4691000000.jpg', 'image_4745000000.jpg', 'image_4603000000.jpg', 'image_4679000000.jpg', 'image_4784000000.jpg', 'image_4822000000.jpg', 'image_4754000000.jpg', 'image_4710000000.jpg', 'image_4686000000.jpg', 'image_4717000000.jpg', 'image_4670000000.jpg', 'image_4736000000.jpg', 'image_4758000000.jpg', 'image_4626000000.jpg', 'image_4741000000.jpg', 'image_4613000000.jpg', 'image_4676000000.jpg', 'image_4643000000.jpg', 'image_4828000000.jpg', 'image_4705000000.jpg', 'image_4711000000.jpg', 'image_4615000000.jpg', 'image_4693000000.jpg'],
['image_778000000.jpg', 'image_779000000.jpg', 'image_792000000.jpg', 'image_787000000.jpg'],
['image_4991000000.jpg', 'image_5005000000.jpg', 'image_4988000000.jpg', 'image_5004000000.jpg', 'image_4998000000.jpg', 'image_4987000000.jpg', 'image_4994000000.jpg'],
['image_752000001.jpg', 'image_836000001.jpg', 'image_855000001.jpg', 'image_637000001.jpg', 'image_826000001.jpg', 'image_678000001.jpg', 'image_868000001.jpg', 'image_732000001.jpg', 'image_743000001.jpg', 'image_734000001.jpg'],
['image_4469000000.jpg', 'image_4476000000.jpg', 'image_4396000000.jpg', 'image_4406000000.jpg', 'image_4463000000.jpg', 'image_4466000000.jpg'],
['image_957000001.jpg', 'image_962000001.jpg', 'image_960000001.jpg'],
['image_278000001.jpg', 'image_274000001.jpg', 'image_283000001.jpg', 'image_242000001.jpg', 'image_277000001.jpg', 'image_280000001.jpg', 'image_233000001.jpg', 'image_265000001.jpg'],
['image_3763000000.jpg', 'image_3776000000.jpg', 'image_3764000000.jpg', 'image_3767000000.jpg', 'image_3773000000.jpg'],
['image_333000001.jpg', 'image_335000001.jpg', 'image_357000001.jpg', 'image_334000001.jpg', 'image_354000001.jpg', 'image_353000001.jpg', 'image_341000001.jpg', 'image_358000001.jpg', 'image_336000001.jpg'],
['image_3738000000.jpg', 'image_3732000000.jpg'],
['image_232000000.jpg'],
['image_995000001.jpg', 'image_999000001.jpg', 'image_988000001.jpg'],
['image_570000001.jpg'],
['image_5011000000.jpg', 'image_5016000000.jpg', 'image_5010000000.jpg', 'image_5015000000.jpg', 'image_5007000000.jpg', 'image_5019000000.jpg'],
['image_3503000001.jpg', 'image_3501000001.jpg'],
['image_1419000000.jpg'],
['image_2304000001.jpg', 'image_2311000001.jpg', 'image_2308000001.jpg', 'image_2306000001.jpg'],
['image_2881000001.jpg', 'image_2893000001.jpg', 'image_2880000001.jpg', 'image_2894000001.jpg', 'image_2888000001.jpg'],
['image_1475000001.jpg', 'image_1489000001.jpg', 'image_1478000001.jpg', 'image_1492000001.jpg', 'image_1468000001.jpg', 'image_1480000001.jpg'],
['image_2776000001.jpg', 'image_2761000001.jpg', 'image_2753000001.jpg', 'image_2760000001.jpg', 'image_2755000001.jpg'],
['image_1853000001.jpg'],
['image_2924000001.jpg', 'image_2902000001.jpg', 'image_2901000001.jpg', 'image_2918000001.jpg', 'image_2913000001.jpg', 'image_2919000001.jpg', 'image_2912000001.jpg'],
['image_2277000000.jpg', 'image_2256000000.jpg', 'image_2328000000.jpg', 'image_2235000000.jpg', 'image_2221000000.jpg', 'image_2244000000.jpg', 'image_2299000000.jpg', 'image_2323000000.jpg', 'image_2262000000.jpg', 'image_2329000000.jpg', 'image_2293000000.jpg', 'image_2287000000.jpg', 'image_2298000000.jpg', 'image_2264000000.jpg', 'image_2270000000.jpg', 'image_2295000000.jpg', 'image_2269000000.jpg', 'image_2349000000.jpg', 'image_2333000000.jpg', 'image_2327000000.jpg', 'image_2290000000.jpg', 'image_2350000000.jpg', 'image_2338000000.jpg', 'image_2231000000.jpg', 'image_2255000000.jpg', 'image_2307000000.jpg', 'image_2288000000.jpg', 'image_2291000000.jpg', 'image_2285000000.jpg', 'image_2351000000.jpg', 'image_2253000000.jpg', 'image_2297000000.jpg'],
['image_3438000001.jpg', 'image_3437000001.jpg'],
['image_2085000000.jpg', 'image_2093000000.jpg'],
['image_1873000000.jpg', 'image_1882000000.jpg', 'image_1902000000.jpg', 'image_1894000000.jpg', 'image_1904000000.jpg', 'image_1870000000.jpg', 'image_1905000000.jpg', 'image_1893000000.jpg'],
['image_2951000001.jpg'],
['image_195000000.jpg', 'image_206000000.jpg', 'image_201000000.jpg', 'image_199000000.jpg'],
['image_969000000.jpg', 'image_975000000.jpg', 'image_973000000.jpg', 'image_967000000.jpg'],
['image_3743000001.jpg', 'image_3748000001.jpg'],
['image_598000000.jpg', 'image_615000000.jpg', 'image_602000000.jpg', 'image_631000000.jpg', 'image_610000000.jpg', 'image_603000000.jpg', 'image_624000000.jpg', 'image_611000000.jpg'],
['image_4996000001.jpg'],
['image_3749000000.jpg', 'image_3740000000.jpg'],
['image_34000000.jpg', 'image_15000000.jpg', 'image_14000000.jpg', 'image_6000000.jpg', 'image_9000000.jpg', 'image_31000000.jpg', 'image_4000000.jpg'],
['image_284000000.jpg', 'image_289000000.jpg', 'image_342000000.jpg', 'image_319000000.jpg', 'image_411000000.jpg', 'image_273000000.jpg', 'image_258000000.jpg', 'image_345000000.jpg', 'image_332000000.jpg', 'image_260000000.jpg', 'image_387000000.jpg', 'image_409000000.jpg', 'image_292000000.jpg', 'image_286000000.jpg', 'image_396000000.jpg', 'image_310000000.jpg', 'image_256000000.jpg', 'image_340000000.jpg', 'image_323000000.jpg', 'image_384000000.jpg', 'image_311000000.jpg', 'image_360000000.jpg', 'image_336000000.jpg', 'image_264000000.jpg'],
['image_4388000001.jpg', 'image_4387000001.jpg'],
['image_4966000000.jpg', 'image_4974000000.jpg', 'image_4967000000.jpg', 'image_4984000000.jpg', 'image_4976000000.jpg', 'image_4971000000.jpg'],
['image_692000000.jpg', 'image_731000000.jpg', 'image_725000000.jpg', 'image_754000000.jpg', 'image_694000000.jpg', 'image_766000000.jpg', 'image_693000000.jpg', 'image_705000000.jpg', 'image_695000000.jpg', 'image_758000000.jpg', 'image_744000000.jpg', 'image_727000000.jpg', 'image_738000000.jpg', 'image_735000000.jpg', 'image_679000000.jpg', 'image_685000000.jpg', 'image_732000000.jpg', 'image_697000000.jpg', 'image_739000000.jpg', 'image_701000000.jpg'],
['image_949000000.jpg', 'image_960000000.jpg', 'image_958000000.jpg', 'image_936000000.jpg', 'image_947000000.jpg', 'image_940000000.jpg'],
['image_48000000.jpg'],
['image_4818000001.jpg', 'image_4721000001.jpg', 'image_4682000001.jpg', 'image_4742000001.jpg', 'image_4738000001.jpg', 'image_4794000001.jpg', 'image_4661000001.jpg', 'image_4768000001.jpg', 'image_4813000001.jpg', 'image_4799000001.jpg', 'image_4771000001.jpg', 'image_4653000001.jpg', 'image_4666000001.jpg', 'image_4739000001.jpg', 'image_4732000001.jpg', 'image_4655000001.jpg', 'image_4713000001.jpg', 'image_4764000001.jpg', 'image_4754000001.jpg', 'image_4731000001.jpg', 'image_4808000001.jpg', 'image_4686000001.jpg', 'image_4767000001.jpg', 'image_4722000001.jpg', 'image_4645000001.jpg', 'image_4724000001.jpg', 'image_4783000001.jpg', 'image_4708000001.jpg', 'image_4729000001.jpg'],
['image_4472000001.jpg', 'image_4483000001.jpg', 'image_4474000001.jpg', 'image_4479000001.jpg', 'image_4473000001.jpg', 'image_4478000001.jpg', 'image_4484000001.jpg'],
['image_802000000.jpg', 'image_806000000.jpg', 'image_793000000.jpg'],
['image_1914000001.jpg', 'image_1977000001.jpg', 'image_1969000001.jpg', 'image_1975000001.jpg', 'image_1930000001.jpg'],
['image_1999000000.jpg'],
['image_2993000001.jpg', 'image_2987000001.jpg', 'image_3001000001.jpg'],
['image_2930000001.jpg', 'image_2940000001.jpg', 'image_2933000001.jpg'],
['image_2201000001.jpg', 'image_2204000001.jpg', 'image_2205000001.jpg', 'image_2175000001.jpg'],
['image_1836000001.jpg', 'image_1838000001.jpg', 'image_1832000001.jpg'],
['image_3498000000.jpg', 'image_3445000000.jpg', 'image_3432000000.jpg', 'image_3457000000.jpg', 'image_3505000000.jpg', 'image_3433000000.jpg', 'image_3456000000.jpg', 'image_3472000000.jpg', 'image_3513000000.jpg', 'image_3512000000.jpg'],
['image_1463000000.jpg'],
['image_2743000001.jpg', 'image_2730000001.jpg'],
['image_1446000000.jpg'],
['image_3469000001.jpg', 'image_3476000001.jpg', 'image_3487000001.jpg', 'image_3471000001.jpg', 'image_3463000001.jpg', 'image_3486000001.jpg', 'image_3488000001.jpg', 'image_3479000001.jpg', 'image_3467000001.jpg'],
['image_2263000001.jpg', 'image_2265000001.jpg', 'image_2271000001.jpg'],
['image_2958000000.jpg', 'image_3029000000.jpg', 'image_3206000000.jpg', 'image_3097000000.jpg', 'image_3024000000.jpg', 'image_3139000000.jpg', 'image_3157000000.jpg', 'image_2895000000.jpg', 'image_3088000000.jpg', 'image_3169000000.jpg', 'image_3219000000.jpg', 'image_2908000000.jpg', 'image_3058000000.jpg', 'image_2923000000.jpg', 'image_3114000000.jpg', 'image_3028000000.jpg', 'image_2937000000.jpg', 'image_3186000000.jpg', 'image_2940000000.jpg', 'image_3127000000.jpg', 'image_3180000000.jpg', 'image_3112000000.jpg', 'image_3106000000.jpg', 'image_2931000000.jpg', 'image_3215000000.jpg', 'image_2901000000.jpg', 'image_3185000000.jpg', 'image_3228000000.jpg', 'image_3122000000.jpg', 'image_3179000000.jpg', 'image_3045000000.jpg', 'image_2920000000.jpg', 'image_3141000000.jpg', 'image_3155000000.jpg', 'image_3069000000.jpg', 'image_2897000000.jpg', 'image_3032000000.jpg', 'image_3204000000.jpg', 'image_3095000000.jpg', 'image_2957000000.jpg', 'image_3026000000.jpg', 'image_3043000000.jpg', 'image_3183000000.jpg', 'image_3062000000.jpg', 'image_3216000000.jpg', 'image_3147000000.jpg', 'image_2891000000.jpg', 'image_3153000000.jpg', 'image_3159000000.jpg', 'image_3050000000.jpg', 'image_3178000000.jpg', 'image_3102000000.jpg', 'image_3068000000.jpg', 'image_2912000000.jpg', 'image_2889000000.jpg', 'image_3021000000.jpg'],
['image_5158000000.jpg'],
['image_3966000001.jpg', 'image_3972000001.jpg', 'image_3960000001.jpg', 'image_3974000001.jpg', 'image_3954000001.jpg', 'image_3970000001.jpg', 'image_3962000001.jpg'],
['image_1285000000.jpg', 'image_1284000000.jpg'],
['image_3961000000.jpg', 'image_3964000000.jpg'],
['image_1369000001.jpg', 'image_1241000001.jpg', 'image_1332000001.jpg', 'image_1217000001.jpg', 'image_1253000001.jpg', 'image_1301000001.jpg', 'image_1205000001.jpg', 'image_1376000001.jpg', 'image_1254000001.jpg', 'image_1368000001.jpg', 'image_1275000001.jpg', 'image_1333000001.jpg', 'image_1350000001.jpg', 'image_1300000001.jpg', 'image_1210000001.jpg', 'image_1231000001.jpg', 'image_1330000001.jpg', 'image_1194000001.jpg', 'image_1305000001.jpg', 'image_1329000001.jpg', 'image_1347000001.jpg', 'image_1293000001.jpg', 'image_1234000001.jpg', 'image_1287000001.jpg', 'image_1322000001.jpg', 'image_1336000001.jpg', 'image_1374000001.jpg', 'image_1232000001.jpg', 'image_1256000001.jpg', 'image_1265000001.jpg', 'image_1323000001.jpg', 'image_1340000001.jpg', 'image_1206000001.jpg'],
['image_5219000001.jpg', 'image_5198000001.jpg', 'image_5151000001.jpg', 'image_5176000001.jpg', 'image_5133000001.jpg', 'image_5177000001.jpg', 'image_5156000001.jpg', 'image_5166000001.jpg', 'image_5202000001.jpg', 'image_5172000001.jpg', 'image_5210000001.jpg', 'image_5204000001.jpg', 'image_5205000001.jpg', 'image_5175000001.jpg'],
['image_4138000001.jpg', 'image_4133000001.jpg'],
['image_1086000000.jpg', 'image_1065000000.jpg', 'image_1050000000.jpg', 'image_1057000000.jpg', 'image_1051000000.jpg', 'image_1069000000.jpg', 'image_1078000000.jpg', 'image_1073000000.jpg', 'image_1058000000.jpg', 'image_1053000000.jpg'],
['image_4227000001.jpg', 'image_4235000001.jpg', 'image_4245000001.jpg', 'image_4246000001.jpg', 'image_4254000001.jpg', 'image_4223000001.jpg', 'image_4255000001.jpg', 'image_4236000001.jpg'],
['image_5023000000.jpg', 'image_5026000000.jpg'],
['image_3574000001.jpg', 'image_3566000001.jpg', 'image_3575000001.jpg', 'image_3573000001.jpg', 'image_3552000001.jpg', 'image_3548000001.jpg', 'image_3545000001.jpg', 'image_3556000001.jpg', 'image_3549000001.jpg', 'image_3565000001.jpg'],
['image_2359000001.jpg', 'image_2354000001.jpg', 'image_2362000001.jpg', 'image_2357000001.jpg'],
['image_1720000001.jpg', 'image_1719000001.jpg'],
['image_3621000000.jpg'],
['image_1698000000.jpg', 'image_1706000000.jpg', 'image_1700000000.jpg', 'image_1696000000.jpg'],
['image_2476000001.jpg', 'image_2462000001.jpg', 'image_2418000000.jpg', 'image_2457000001.jpg', 'image_2471000001.jpg', 'image_2494000001.jpg', 'image_2488000001.jpg', 'image_2485000001.jpg', 'image_2453000001.jpg', 'image_2454000001.jpg', 'image_2489000001.jpg', 'image_2475000001.jpg', 'image_2416000000.jpg'],
['image_2682000001.jpg', 'image_2685000001.jpg'],
['image_2507000000.jpg', 'image_2506000000.jpg'],
['image_1641000000.jpg'],
['image_2727000000.jpg', 'image_2712000000.jpg', 'image_2684000000.jpg', 'image_2721000000.jpg', 'image_2696000000.jpg', 'image_2682000000.jpg', 'image_2674000000.jpg', 'image_2713000000.jpg', 'image_2745000000.jpg', 'image_2691000000.jpg', 'image_2734000000.jpg', 'image_2686000000.jpg', 'image_2728000000.jpg', 'image_2699000000.jpg', 'image_2702000000.jpg', 'image_2694000000.jpg', 'image_2705000000.jpg', 'image_2687000000.jpg', 'image_2729000000.jpg', 'image_2669000000.jpg'],
['image_2494000000.jpg'],
['image_3654000000.jpg', 'image_3637000000.jpg', 'image_3647000000.jpg', 'image_3660000000.jpg', 'image_3658000000.jpg', 'image_3650000000.jpg'],
['image_1626000000.jpg', 'image_1627000000.jpg', 'image_1622000000.jpg', 'image_1629000000.jpg', 'image_1630000000.jpg', 'image_1623000000.jpg'],
['image_1019000000.jpg', 'image_1027000000.jpg', 'image_1009000000.jpg', 'image_1022000000.jpg', 'image_1036000000.jpg', 'image_1024000000.jpg'],
['image_5020000001.jpg'],
['image_4193000001.jpg', 'image_4195000001.jpg', 'image_4179000001.jpg', 'image_4174000001.jpg', 'image_4216000001.jpg'],
['image_1225000000.jpg'],
['image_4159000000.jpg', 'image_4173000000.jpg'],
['image_5150000000.jpg'],
['image_3983000000.jpg', 'image_3979000000.jpg', 'image_3985000000.jpg', 'image_3989000000.jpg', 'image_3987000000.jpg'],
['image_5197000001.jpg', 'image_5183000001.jpg', 'image_5188000001.jpg', 'image_5196000001.jpg'],
['image_1386000001.jpg', 'image_1388000001.jpg', 'image_1384000001.jpg', 'image_1389000001.jpg'],
['image_3921000000.jpg'],
['image_2667000001.jpg', 'image_2665000001.jpg', 'image_2664000001.jpg'],
['image_2497000001.jpg', 'image_2500000001.jpg'],
['image_1613000000.jpg', 'image_1609000000.jpg'],
['image_3682000000.jpg', 'image_3666000000.jpg'],
['image_2583000001.jpg', 'image_2574000001.jpg', 'image_2531000001.jpg', 'image_2567000001.jpg', 'image_2603000001.jpg', 'image_2554000001.jpg', 'image_2564000001.jpg', 'image_2545000001.jpg', 'image_2534000001.jpg', 'image_2593000001.jpg', 'image_2515000001.jpg', 'image_2539000001.jpg', 'image_2571000001.jpg', 'image_2592000001.jpg', 'image_2577000001.jpg'],
['image_1647000000.jpg', 'image_1646000000.jpg'],
['image_3631000001.jpg', 'image_3647000001.jpg', 'image_3624000001.jpg', 'image_3621000001.jpg', 'image_3626000001.jpg', 'image_3648000001.jpg', 'image_3639000001.jpg'],
['image_2457000000.jpg', 'image_2432000000.jpg', 'image_2456000000.jpg', 'image_2525000000.jpg', 'image_2465000000.jpg', 'image_2460000000.jpg', 'image_2474000000.jpg', 'image_2466000000.jpg', 'image_2461000000.jpg', 'image_2512000000.jpg'],
['image_2712000001.jpg', 'image_2696000001.jpg', 'image_2720000001.jpg', 'image_2692000001.jpg', 'image_2702000001.jpg', 'image_2694000001.jpg', 'image_2695000001.jpg'],
['image_1711000001.jpg', 'image_1703000001.jpg', 'image_1698000001.jpg', 'image_1710000001.jpg'],
['image_3529000000.jpg', 'image_3526000000.jpg', 'image_3521000000.jpg', 'image_3542000000.jpg'],
['image_1736000000.jpg', 'image_1741000000.jpg', 'image_1731000000.jpg', 'image_1737000000.jpg', 'image_1720000000.jpg', 'image_1715000000.jpg', 'image_1712000000.jpg'],
['image_2321000001.jpg', 'image_2313000001.jpg', 'image_2320000001.jpg', 'image_2318000001.jpg', 'image_2339000001.jpg'],
['image_1359000000.jpg'],
['image_5242000001.jpg', 'image_5245000001.jpg', 'image_5248000001.jpg', 'image_5240000001.jpg', 'image_5237000001.jpg', 'image_5246000001.jpg', 'image_5236000001.jpg'],
['image_1724000001.jpg', 'image_1722000001.jpg'],
['image_1335000000.jpg'],
['image_5287000001.jpg', 'image_5289000001.jpg', 'image_5259000001.jpg', 'image_5291000001.jpg'],
['image_1724000000.jpg', 'image_1725000000.jpg'],
['image_1513000000.jpg', 'image_1510000000.jpg', 'image_1516000000.jpg'],
['image_2124000000.jpg', 'image_2125000000.jpg', 'image_2128000000.jpg'],
['image_2807000001.jpg', 'image_2806000001.jpg', 'image_2817000001.jpg'],
['image_1404000000.jpg', 'image_1405000000.jpg', 'image_1406000000.jpg'],
['image_2870000001.jpg', 'image_2869000001.jpg', 'image_2871000001.jpg', 'image_2877000001.jpg', 'image_2874000001.jpg'],
['image_2022000000.jpg'],
['image_1963000000.jpg'],
['image_3012000001.jpg'],
['image_1533000000.jpg', 'image_1535000000.jpg', 'image_1531000000.jpg'],
['image_1797000000.jpg', 'image_1810000000.jpg', 'image_1825000000.jpg', 'image_1816000000.jpg', 'image_1805000000.jpg', 'image_1803000000.jpg', 'image_1819000000.jpg', 'image_1814000000.jpg'],
['image_2068000000.jpg'],
['image_3316000000.jpg', 'image_3277000000.jpg', 'image_3382000000.jpg', 'image_3292000000.jpg', 'image_3379000000.jpg', 'image_3360000000.jpg', 'image_3281000000.jpg', 'image_3248000000.jpg', 'image_3311000000.jpg', 'image_3243000000.jpg', 'image_3293000000.jpg', 'image_3372000000.jpg', 'image_3287000000.jpg', 'image_3329000000.jpg', 'image_3314000000.jpg', 'image_3321000000.jpg', 'image_3363000000.jpg', 'image_3380000000.jpg', 'image_3306000000.jpg', 'image_3344000000.jpg', 'image_3237000000.jpg', 'image_3371000000.jpg', 'image_3290000000.jpg', 'image_3315000000.jpg', 'image_3301000000.jpg', 'image_3297000000.jpg', 'image_3376000000.jpg', 'image_3339000000.jpg', 'image_3274000000.jpg', 'image_3348000000.jpg', 'image_3307000000.jpg', 'image_3345000000.jpg', 'image_3258000000.jpg', 'image_3285000000.jpg'],
['image_4922000001.jpg', 'image_4925000001.jpg', 'image_4946000001.jpg', 'image_4954000001.jpg', 'image_4943000001.jpg', 'image_4938000001.jpg'],
['image_4323000001.jpg', 'image_4337000001.jpg', 'image_4352000001.jpg', 'image_4328000001.jpg', 'image_4355000001.jpg', 'image_4329000001.jpg', 'image_4366000001.jpg', 'image_4321000001.jpg', 'image_4392000001.jpg', 'image_4363000001.jpg', 'image_4349000001.jpg', 'image_4320000001.jpg', 'image_4370000001.jpg', 'image_4364000001.jpg'],
['image_906000001.jpg', 'image_908000001.jpg', 'image_905000001.jpg', 'image_904000001.jpg'],
['image_4529000000.jpg', 'image_4523000000.jpg', 'image_4526000000.jpg', 'image_4527000000.jpg'],
['image_4876000001.jpg', 'image_4877000001.jpg'],
['image_3817000001.jpg', 'image_3829000001.jpg', 'image_3824000001.jpg'],
['image_891000000.jpg', 'image_885000000.jpg', 'image_874000000.jpg', 'image_878000000.jpg', 'image_890000000.jpg', 'image_876000000.jpg'],
['image_3683000000.jpg', 'image_3685000000.jpg'],
['image_141000000.jpg', 'image_179000000.jpg', 'image_152000000.jpg', 'image_131000000.jpg', 'image_125000000.jpg', 'image_178000000.jpg', 'image_159000000.jpg', 'image_151000000.jpg', 'image_132000000.jpg'],
['image_501000000.jpg'],
['image_64000000.jpg', 'image_95000000.jpg', 'image_65000000.jpg', 'image_71000000.jpg', 'image_85000000.jpg', 'image_54000000.jpg', 'image_78000000.jpg', 'image_90000000.jpg', 'image_84000000.jpg', 'image_96000000.jpg'],
['image_3780000001.jpg', 'image_3776000001.jpg', 'image_3779000001.jpg', 'image_3783000001.jpg'],
['image_385000001.jpg'],
['image_4596000000.jpg', 'image_4593000000.jpg', 'image_4595000000.jpg'],
['image_2177000000.jpg', 'image_2175000000.jpg'],
['image_1810000001.jpg', 'image_1816000001.jpg', 'image_1808000001.jpg', 'image_1822000001.jpg', 'image_1819000001.jpg'],
['image_3408000001.jpg', 'image_3409000001.jpg'],
['image_1942000000.jpg', 'image_1946000000.jpg'],
['image_2016000000.jpg', 'image_2015000000.jpg'],
['image_1599000000.jpg', 'image_1600000000.jpg'],
['image_3009000001.jpg', 'image_3004000001.jpg'],
['image_1395000000.jpg', 'image_1398000000.jpg', 'image_1402000000.jpg', 'image_1392000000.jpg'],
['image_2843000001.jpg', 'image_2836000001.jpg', 'image_2846000001.jpg'],
['image_1518000001.jpg', 'image_1516000001.jpg'],
['image_2845000000.jpg', 'image_2818000000.jpg', 'image_2834000000.jpg', 'image_2820000000.jpg', 'image_2812000000.jpg', 'image_2842000000.jpg', 'image_2814000000.jpg', 'image_2808000000.jpg', 'image_2860000000.jpg', 'image_2855000000.jpg', 'image_2817000000.jpg', 'image_2859000000.jpg'],
['image_2169000001.jpg', 'image_2113000001.jpg', 'image_2107000001.jpg', 'image_2017000001.jpg', 'image_2145000001.jpg', 'image_2164000001.jpg', 'image_2091000001.jpg', 'image_2053000001.jpg', 'image_2115000001.jpg', 'image_2097000001.jpg', 'image_2143000001.jpg', 'image_2075000001.jpg', 'image_2061000001.jpg', 'image_2106000001.jpg', 'image_1987000001.jpg', 'image_2078000001.jpg', 'image_2016000001.jpg', 'image_2114000001.jpg', 'image_2010000001.jpg', 'image_2057000001.jpg', 'image_2105000001.jpg', 'image_2108000001.jpg', 'image_2158000001.jpg', 'image_2070000001.jpg', 'image_2051000001.jpg', 'image_2098000001.jpg', 'image_2069000001.jpg', 'image_2095000001.jpg', 'image_2032000001.jpg', 'image_1991000001.jpg', 'image_2019000001.jpg', 'image_2152000001.jpg', 'image_2123000001.jpg', 'image_2050000001.jpg', 'image_2099000001.jpg', 'image_1997000001.jpg', 'image_2006000001.jpg', 'image_2012000001.jpg', 'image_2068000001.jpg', 'image_2049000001.jpg', 'image_2027000001.jpg'],
['image_3807000000.jpg', 'image_3822000000.jpg', 'image_3805000000.jpg'],
['image_20000001.jpg', 'image_42000001.jpg', 'image_36000001.jpg', 'image_24000001.jpg', 'image_59000001.jpg'],
['image_4536000001.jpg', 'image_4591000001.jpg', 'image_4583000001.jpg', 'image_4553000001.jpg', 'image_4559000001.jpg', 'image_4537000001.jpg', 'image_4584000001.jpg', 'image_4554000001.jpg', 'image_4561000001.jpg', 'image_4587000001.jpg', 'image_4542000001.jpg'],
['image_467000001.jpg'],
['image_175000001.jpg', 'image_177000001.jpg', 'image_186000001.jpg'],
['image_3700000001.jpg', 'image_3684000001.jpg', 'image_3679000001.jpg'],
['image_548000000.jpg', 'image_576000000.jpg', 'image_594000000.jpg', 'image_568000000.jpg', 'image_592000000.jpg', 'image_493000000.jpg', 'image_528000000.jpg', 'image_578000000.jpg'],
['image_4857000000.jpg', 'image_4887000000.jpg', 'image_4908000000.jpg', 'image_4925000000.jpg', 'image_4910000000.jpg', 'image_4886000000.jpg', 'image_4940000000.jpg', 'image_4926000000.jpg', 'image_4945000000.jpg', 'image_4906000000.jpg', 'image_4861000000.jpg', 'image_4927000000.jpg', 'image_4933000000.jpg', 'image_4900000000.jpg', 'image_4942000000.jpg'],
['image_4503000000.jpg', 'image_4502000000.jpg', 'image_4499000000.jpg', 'image_4494000000.jpg', 'image_4510000000.jpg', 'image_4509000000.jpg', 'image_4491000000.jpg', 'image_4500000000.jpg', 'image_4514000000.jpg', 'image_4496000000.jpg', 'image_4490000000.jpg'],
['image_866000000.jpg', 'image_860000000.jpg'],
['image_3832000000.jpg', 'image_3848000000.jpg', 'image_3842000000.jpg', 'image_3850000000.jpg', 'image_3844000000.jpg', 'image_3833000000.jpg', 'image_3855000000.jpg', 'image_3830000000.jpg', 'image_3854000000.jpg'],
['image_4328000000.jpg'],
['image_4960000001.jpg', 'image_4961000001.jpg', 'image_4987000001.jpg', 'image_4976000001.jpg', 'image_4965000001.jpg', 'image_4986000001.jpg'],
['image_921000000.jpg', 'image_916000000.jpg']]

labels = [[1], [1], [0], [0], [1], [1], [1], [0], [0], [1], [0], [0], [0], [1], [1], [1], [0], [0], [0], [0], [0], [0], [0], [1], [1], [1], [0], [0], [0], [0], [0], [0], [1], [0], [1], [0], [0], [1], [0], [0], [1], [1], [0], [1], [0], [0], [1], [1], [1], [1], [0], [0], [0], [1], [0], [1], [1], [0], [1], [0], [0], [1], [1], [0], [1], [0], [1], [1], [1], [1], [1], [1], [0], [1], [0], [0], [1], [0], [0], [1], [0], [1], [0], [0], [0], [1], [0], [0], [0], [0], [1], [1], [0], [1], [0], [1], [1], [1], [1], [0], [0], [1], [0], [1], [1], [0], [0], [1], [0], [0], [1], [1], [1], [0], [1], [0], [1], [1], [1], [0], [0], [1], [1], [0], [0], [0], [0], [0], [0], [0], [1], [1], [0], [0], [0], [0], [1], [1], [0], [1], [1], [0], [0], [1], [0], [1], [0], [1], [1], [0], [0], [1], [0], [1], [1], [0], [1], [0], [0], [0], [1], [0], [1], [0], [0], [1], [0], [0], [0], [0], [1], [1], [1], [0], [1], [1], [0], [0], [1], [0], [0], [1], [1], [0], [0], [1], [1], [0], [0], [0], [1], [0], [1], [1], [0], [1], [0], [1], [1], [1], [1], [1], [0], [0], [0], [0], [0], [0], [1], [0]]

# Mosquitto 
# LOCAL_MQTT_HOST = "mosquitto-service"
LOCAL_MQTT_HOST = "mosquitto"
LOCAL_MQTT_PORT = 1883
LOCAL_IMAGE_TOPIC = "image_topic"
#LOCAL_NOTIF_TOPIC = "model_output_topic"
PUBLISH_TOPIC = LOCAL_IMAGE_TOPIC
#PUBLISH_TOPIC = LOCAL_NOTIF_TOPIC

local_mqttclient = mqtt.Client()

# Setup Local MQTT callbacks
def on_connect_local(client, userdata, flags, rc):
    print("connected to ", PUBLISH_TOPIC, " with rc: " + str(rc))

def on_disconnect_local(client, userdata, flags, rc): 
    print("Disconnected from local broker, result code" + str(rc))
    global local_mqttclient 
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_publish_local(client, userdata, msg_id):
    print("Message successfully published: {}".format(msg_id))

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
        path = "/data/door_cam_images/images/"
        # publish all events to the queue
        for event in events:
            for ndx in range(len(event)):
                filename=event[ndx]
                mesg = "{};{};{}".format(vid_source, path, filename)
                local_mqttclient.publish(topicName, mesg)
                print("Message written: ", mesg)
                # messages are written once every second; sleep for 80th percent of time
                time.sleep(0.8)
            
            # after every event, wait for a random amount of time (between 15 and 20 seconds)
            random_sleep_time = random.randint(8, 14)
            time.sleep(random_sleep_time)
    except:
      print("Unexpected error:", sys.exc_info()[0])

def run():
    # Make connections to local broker
    global local_mqttclient 

    local_mqttclient.on_connect = on_connect_local
    local_mqttclient.on_publish = on_publish_local
    local_mqttclient.on_disconnect = on_disconnect_local

    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
    print("Topic to be published to: ", PUBLISH_TOPIC)
    publishDataToModel(PUBLISH_TOPIC)


def main():
    run()

if __name__ == "__main__":
    main()
