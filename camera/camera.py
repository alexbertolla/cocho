import time
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

    cv.putText(roi_draw, f"{center_pixel_distance}mm", (width_center, height_center), cv.FONT_HERSHEY_PLAIN, 2,
               (0, 17, 255), 2)

    roi_color_frame = color_frame[int(height_center - limit_height_roi):int(height_center + limit_height_roi),
                      int(width_center - limit_width_roi):int(width_center + limit_width_roi), :]

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
            color_roi_draw, roi_color_image = draw_roi(color_image, camera_object.limit_width_roi,
                                                       camera_object.limit_height_roi, distance_object)
            #if distance_object > camera_object.min_distance and distance_object <= camera_object.max_distance:
            #    camera_object.save_frame(color_image, counter, "original")
            #    camera_object.save_point_cloud(depth_frame, counter, "original")
            #    camera_object.save_frame(depth_colormap, counter, "color_map")

            camera_object.frame_show = color_roi_draw

            counter += 1


def stop(camera):
    cv.destroyAllWindows()
    camera.stop_camera()


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
        return {"camera_name": self.__camera_name,
                "serial_number": self.__serial_number,
                "min_distance": self.min_distance,
                "max_distance": self.max_distance,
                "width": self.width,
                "height": self.height,
                "fps": self.fps}

    @property
    def get_name(self):
        return self.__camera_name

    @property
    def get_serial_number(self):
        return self.__serial_number
