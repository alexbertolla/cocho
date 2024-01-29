'''
Created on 22 de set. de 2023

@author: alex.bertolla
'''

import pyrealsense2 as rs

ctx = rs.context()
devices = ctx.query_devices()

for devicen_num, device in enumerate(devices):
    print(f"Camera {devicen_num}: {device}")

print("Fisnish")
