import sys
import cv2

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries()

    # Modify camera configuration
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_OFF
    # print(device_config)

    # Start device
    deviceL = pykinect.start_device(0, config=device_config)
    deviceR = pykinect.start_device(1, config=device_config)
    cv2.namedWindow('Color Image L', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Color Image R', cv2.WINDOW_NORMAL)

    index = 0
    while True:

        captureL = deviceL.update()
        retL, color_image_L = captureL.get_color_image()
        cv2.imshow("Color Image L", color_image_L)

        captureR = deviceR.update()
        retR, color_image_R = captureR.get_color_image()
        cv2.imshow("Color Image R", color_image_R)

        if not retL:
            if not retR:
                continue

        # Plot the image

        # Press key
        if cv2.waitKey(1) & 0xFF == ord('p'):  # 如果按下p 就截图保存并退出
            cv2.imwrite("../calibrationPic/L/Left" + str(index) + ".png", color_image_L)  # 保存路径
            print("have saved picture " + "../calibrationPic/L/Left" + str(index) + ".png")
            cv2.imwrite("../calibrationPic/R/Right" + str(index) + ".png", color_image_R)  # 保存路径
            print("have saved picture " + "../calibrationPic/R/Right" + str(index) + ".png")
            index = index + 1
        elif cv2.waitKey(3) & 0xFF == ord('q'):

            break
