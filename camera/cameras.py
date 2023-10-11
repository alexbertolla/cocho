'''
Created on 31 de ago. de 2023
@author: alex.bertolla
'''
from camera.intelrealsense import IntelRealsense
import cv2 as cv
import numpy as np
from threading import Thread


def draw_roi(color_frame, limit_width_roi, limit_height_roi, center_pixel_distance):
    # .shape => Largura, Altura e Dimenssão
    height, width, _ = color_frame.shape
    roi_frame = np.copy(color_frame)
    
    width_center = int(width / 2)
    height_center = int(height / 2)
    
    # frame_center = (int(width / 2), int(height / 2))
    # Para desenhar figuras Lagura, Altura
    roi_xy1 = (int(width_center - limit_width_roi), int(height_center - limit_height_roi))
    roi_xy2 = (int(width_center + limit_width_roi), int(height_center + limit_height_roi))
    cv.circle(roi_frame, (width_center, height_center), 1, (0, 255, 0), 5)
    
    roi_draw = cv.rectangle(roi_frame, roi_xy1, roi_xy2, (0, 0, 255), 2)
    
    cv.putText(roi_draw, f"{center_pixel_distance}mm", (width_center, height_center), cv.FONT_HERSHEY_PLAIN, 2, (0, 17, 255), 2)
    
    roi_color_frame = color_frame[int(height_center - limit_height_roi):int(height_center + limit_height_roi), int(width_center - limit_width_roi):int(width_center + limit_width_roi),:]
    
    return roi_draw, roi_color_frame


def record(camera_object):
   
    if camera_object:
        camera_object.start_camera()
        camera_object.get_info()
    
    counter = 0
    
    while True:
        if not camera_object.running:
            break
        else:
            capture_frame, depth_colormap, color_image, depth_image, depth_frame = camera_object.get_frame()
            distance_object = camera_object.calculate_center_pixel_distance(depth_image)
            color_roi_draw, roi_color_image = draw_roi(color_image, camera_object.limit_width_roi, camera_object.limit_height_roi, distance_object)
            
            if distance_object > camera_object.min_distance and distance_object <= camera_object.max_distance:
                camera_object.save_frame(color_image, counter, "original")
                camera_object.save_frame(roi_color_image, counter, "roi")
                camera_object.save_frame(depth_colormap, counter, "color_map")
                camera_object.save_point_cloud(depth_frame, counter, "original")
            
            camera_object.frame_show = color_roi_draw
        
        # if not capture:
        #    print("ERRO")
        #    exit(0)
        
        counter += 1


class camera(IntelRealsense):

    def __init__(self, camera_name, fps=5, width=848, height=480):

        if camera_name == "face":
            self.__camera_name = "Face"
            self.__serial_number = "241122307171"
            self.limit_width_roi = 200
            self.limit_height_roi = 200
            self.min_distance = 900
            self.max_distance = 1300 

        elif camera_name == "dorso":
            self.__camera_name = "Dorso"
            self.__serial_number = "234222302668"
            self.limit_width_roi = 350
            self.limit_height_roi = 200
            self.min_distance = 850
            self.max_distance = 1100

        elif camera_name == "barriga":
            self.__camera_name = "Barriga"
            self.__serial_number = "234222302236"  # "234222300086"
            self.limit_width_roi = 200
            self.limit_height_roi = 200
            self.min_distance = 550
            self.max_distance = 700

        else:
            print("Invalid camera type")
            exit(0)
        
        self.width = width
        self.height = height
        self.fps = fps
        IntelRealsense.__init__(self, self.__serial_number, width, height, fps)
    
    @property
    def camera_info(self):
        return {"camera_name":self.__camera_name,
                "serial_number":self.__serial_number,
                "min_distance":self.min_distance,
                "max_distance":self.max_distance,
                "width":self.width,
                "height":self.height,
                "fps":self.fps}
    
    @property
    def get_name(self):
        return self.__camera_name

    @property
    def get_serial_number(self):
        return self.__serial_number


frame_captured = None
window_name = "Frames Captured: "

if __name__ == '__main__':
    try:
        cam_face = camera(camera_name="face", fps=30)
        cam_dorso = camera(camera_name="dorso", fps=30)
        cam_barriga = camera(camera_name="barriga", fps=30)
        
        # record(camera_face=None, camera_dorso=cam_dorso, camera_barriga=None) 
        # record(camera=cam_dorso)
        # record(camera=cam_barriga)
        
        th_face = Thread(target=record, args=(cam_face,))
        th_dorso = Thread(target=record, args=(cam_dorso,))
        th_barriga = Thread(target=record, args=(cam_barriga,))
        
        th_face.start(), th_face.join(timeout=1)
        th_dorso.start(), th_dorso.join(timeout=1)
        th_barriga.start(), th_barriga.join(timeout=1)

        while th_face.is_alive() or th_dorso.is_alive():
            frame_captured = np.hstack((cam_face.frame_show, cam_dorso.frame_show, cam_barriga.frame_show))
            
            cv.namedWindow(window_name, cv.WND_PROP_FULLSCREEN)
            cv.setWindowProperty(window_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow(window_name, frame_captured)
            
            key = cv.waitKey(3)
            if key == 27:
                cv.destroyAllWindows()
                
                cam_face.stop_camera()
                cam_dorso.stop_camera()
                cam_barriga.stop_camera()
                
                break
        
    except ValueError:
        print("ERROR")
        print(ValueError)
        pass
    
    print('FINISH')
