import sys
import cv2

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries()

    # Modify camera configuration
    device_config = pykinect.default_configuration
    device_config.synchronized_images_only = True
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
    print("device_config: ")
    print(device_config)

    # Start device
    video_filename0 = "../data/output0.mkv"

    device0 = pykinect.start_device(0, config=device_config, record=True, record_filepath=video_filename0)

    cv2.namedWindow('Image0', cv2.WINDOW_NORMAL)

    while True:

        # Get capture
        capture0 = device0.update()
        ret0, color_image0 = capture0.get_color_image()
        if not ret0:
            continue

        cv2.imshow('Image0', color_image0)

        # Plot the image

        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break
