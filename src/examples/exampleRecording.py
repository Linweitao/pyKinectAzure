import sys
import cv2

sys.path.insert(1, '../../')
import pykinect_azure as pykinect

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
	#print(device_config)

	# Start device
	video_filename = "C:/Users/59335/Desktop/3dhuman/output.mkv"
	device = pykinect.start_device(0, config=device_config, record=True, record_filepath=video_filename)

	cv2.namedWindow('Depth Image',cv2.WINDOW_NORMAL)
	while True:

		# Get capture
		capture = device.update()

		# Get the color depth image from the capture
		ret, depth_image = capture.get_colored_depth_image()

		if not ret:
			continue
			
		# Plot the image
		cv2.imshow('Depth Image',depth_image)
		
		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):  
			break