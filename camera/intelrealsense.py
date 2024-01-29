'''
Created on 13 de set. de 2023

@author: alex.bertolla
'''

import numpy as np
import cv2 as cv
import pyrealsense2 as rs
import tifffile as tiff
from datetime import datetime
from os import path
import os
    

class IntelRealsense:

    def __init__(self, serial_number, width, height, fps):
       
        self.camera_pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device(serial_number)
        self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
        self.config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)

        self.running = False
        self.frame_show = None
        # self.start_camera()
        
    def start_camera(self):
        print(f"Starting camera {self.get_name}")
        self.profile = self.camera_pipeline.start(self.config)
        self.running = True
        print(f"Camera {self.get_name} started ")
        
    def stop_camera(self):
        print(f"Stopping Camera {self.get_name}")
        self.running = False
        self.camera_pipeline.stop()
    
    def get_camera_status(self):
        return self.running
    
    def get_info(self):
        
        if not self.camera_pipeline:
            print(f"Camera {self.get_name} not started yet")
            return False
            
        pipeline_wrapper = rs.pipeline_wrapper(self.camera_pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()

        print(self.camera_info)
        print(self.camera_pipeline)
        print(pipeline_wrapper)
        print(pipeline_profile)
        print(device)
        print("---------")
        
    def get_frame(self):
        
        if not self.running:
            print(f"Camera {self.get_name} is not working")
            return False, None, None, None
        # else:
        #    print(f"Getting frame from camera {self.get_name}")
        
        align_to = rs.stream.color
        align = rs.align(align_to)
            
        # Get frameset of color and depth
        frames = self.camera_pipeline.wait_for_frames(timeout_ms=10000)
        
        # Align the depth frame to color frame
        aligned_frames = align.process(frames)
        
        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()
        
        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            return False
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.01), cv.COLORMAP_JET)
        return True, depth_colormap, color_image, depth_image, aligned_depth_frame
    
    def calculate_center_pixel_distance(self, depth_frame):
        height, width = depth_frame.shape
        frame_center = (int(width / 2), int(height / 2))
        return depth_frame[frame_center[1], frame_center[0]]
    
    def save_frame(self, frame, counter, tipo):
        directory = f"{self.get_serial_number}_{tipo}"
        if not path.exists(directory):
            print(f"Directory {directory} created")
            os.mkdir(directory)
        
        # if center_pixel_distance > self.min_distance and center_pixel_distance <= self.max_distance:
        prefix = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{counter}"
        filename = f"./{directory}/{prefix}.tiff"
               
        tiff.imsave(filename, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        print(f"File {filename} saved")
    
    def save_point_cloud(self, depth_frame, counter, tipo):
        directory = f"{self.get_serial_number}_{tipo}_point_cloud"
        if not path.exists(directory):
            print(f"Directory {directory} created")
            os.mkdir(directory)
            
        point_cloud = rs.pointcloud()
        points = point_cloud.calculate(depth_frame)
        point_cloud.map_to(depth_frame)
        
        # Pointcloud data to arrays
        v, t = points.get_vertices(), points.get_texture_coordinates()
        verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
        texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv
        
        prefix = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{counter}"
        filename = f"./{directory}/{prefix}.ply"
        points.export_to_ply(filename, depth_frame)

