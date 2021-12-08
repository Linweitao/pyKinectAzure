import sys
import cv2

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries()

    # Modify camera configuration
    # 设置相机参数
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
    print("device_config: ")
    print(device_config)

    # Start device
    video_filenameL = "../data/outputL.mkv"
    video_filenameR = "../data/outputR.mkv"
    deviceL = pykinect.start_device(0, config=device_config, record=True, record_filepath=video_filenameL)
    deviceR = pykinect.start_device(1, config=device_config, record=True, record_filepath=video_filenameR)

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
