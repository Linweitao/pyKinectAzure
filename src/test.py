import json

import cv2
import numpy as np
from matplotlib import pyplot as plt

from pykinect_azure import pykinect, k4abt_body2D_t, k4abt_body_t, Body, Body2d
from src.tool import Camera3dTo2dByK, Camera3dTo3dCoordinateConversion, Camera3dTo2dByKinectSDK

# [1101.110595703125, 325.7978515625]
# [376.4811096191406, -596.359375, 2459.72314453125]
# position3d = np.array([519.243408203125, -184.34524536132812, 987.3510131835938])
# filename = 'camera_calibration'
# with open(filename) as file_obj:
#     line = file_obj.readline()
#     ccdata = json.loads(line)
#     T = ccdata['T']
#     R = ccdata['R']
# position3d = Camera3dTo3dCoordinateConversion(position3d, R, T, 1)
# print(position3d)
mtx1 = np.array(
    [[915.3875732421875, 0.0, 959.9261474609375], [0.0, 914.9352416992188, 549.2899169921875], [0.0, 0.0, 1.0]])
# position2d = Camera3dTo2dCoordinateConversion(position3d, mtx1)
# print(position2d)

camera = "L"
video_filename = "../data/output" + camera + ".mkv"

pts3d = [[381.1416320800781, -59.284976959228516, 2450.524169921875],
         [376.26483154296875, -237.43312072753906, 2439.35205078125],
         [375.85040283203125, -380.1771545410156, 2437.73291015625]]
print(Camera3dTo2dByKinectSDK(video_filename, pts3d))
