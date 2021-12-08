import sys

from pykinect_azure import pykinect
sys.path.insert(1, '../')
import pykinect_azure as pykinect

pykinect.initialize_libraries()

# Modify camera configuration
# 设置相机参数
device_config = pykinect.default_configuration
device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
print("device_config: ")
print(device_config)

deviceL = pykinect.start_device(0, config=device_config)
# deviceR = pykinect.start_device(1, config=device_config)

c1 = deviceL.get_calibration(pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED,pykinect.K4A_COLOR_RESOLUTION_1080P)
# c2 = deviceR.get_calibration(pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED,pykinect.K4A_COLOR_RESOLUTION_1080P)
print("cameraL")
print (c1._handle.color_camera_calibration.intrinsics.parameters.param.fx," ",c1._handle.color_camera_calibration.intrinsics.parameters.param.fy)
print (c1._handle.color_camera_calibration.intrinsics.parameters.param.cx," ",c1._handle.color_camera_calibration.intrinsics.parameters.param.cy)
# print("cameraR")
# print (c2._handle.color_camera_calibration.intrinsics.parameters.param.fx," ",c2._handle.color_camera_calibration.intrinsics.parameters.param.fy)
# print (c2._handle.color_camera_calibration.intrinsics.parameters.param.cx," ",c2._handle.color_camera_calibration.intrinsics.parameters.param.cy)