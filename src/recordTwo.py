import sys
import cv2
import time
sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries()

    # 设置右相机参数
    device_configR = pykinect.default_configuration
    device_configR.synchronized_images_only = True
    device_configR.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
    device_configR.wired_sync_mode = pykinect.K4A_WIRED_SYNC_MODE_SUBORDINATE
    device_configR.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
    video_filenameR = "../data/outputR.mkv"
    deviceR = pykinect.start_device(1, config=device_configR, record=True, record_filepath=video_filenameR)
    time.sleep(2)
    # 设置左相机参数
    device_configL = pykinect.default_configuration
    device_configL.synchronized_images_only = True
    device_configL.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
    device_configL.wired_sync_mode = pykinect.K4A_WIRED_SYNC_MODE_MASTER
    device_configL.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
    video_filenameL = "../data/outputL.mkv"
    deviceL = pykinect.start_device(0, config=device_configL, record=True, record_filepath=video_filenameL)




    cv2.namedWindow('ImageL', cv2.WINDOW_NORMAL)
    cv2.namedWindow('ImageR', cv2.WINDOW_NORMAL)
    while True:

        # Get capture
        captureL = deviceL.update()
        retL, color_imageL = captureL.get_color_image()
        if not retL:
            continue
        captureR = deviceR.update()
        retR, color_imageR = captureR.get_color_image()
        if not retR:
            continue

        cv2.imshow('ImageL', color_imageL)
        cv2.imshow('ImageR', color_imageR)

        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break
