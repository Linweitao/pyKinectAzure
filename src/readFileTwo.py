import sys
import cv2
import json

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

    video_filenameL = "../data/outputL.mkv"
    video_filenameR = "../data/outputR.mkv"
    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    # Start playback
    playbackL = pykinect.start_playback(video_filenameL)
    playbackR = pykinect.start_playback(video_filenameR)

    playback_config_L = playbackL.get_record_configuration()
    playback_config_R = playbackR.get_record_configuration()
    # print(playback_config)

    playback_calibration_L = playbackL.get_calibration()
    playback_calibration_R = playbackR.get_calibration()

    # Start body tracker
    bodyTrackerL = pykinect.start_body_tracker(calibration=playback_calibration_L)
    bodyTrackerR = pykinect.start_body_tracker(calibration=playback_calibration_R)

    cv2.namedWindow('combined_imageL', cv2.WINDOW_NORMAL)
    cv2.namedWindow('combined_imageR', cv2.WINDOW_NORMAL)
    index = 0
    while playbackL.isOpened():
        index = index + 1
        # Get camera capture
        captureL = playbackL.update()
        captureR = playbackR.update()
        # Get body tracker frame
        body_frame_L = bodyTrackerL.update(capture=captureL)
        body_frame_R = bodyTrackerR.update(capture=captureR)
        # 获得关节点
        num_bodiesL, jointsL = body_frame_L.get_body_joints_CameraOfColor()
        num_bodiesR, jointsR = body_frame_R.get_body_joints_CameraOfColor()
        retL, color_image_L = captureL.get_color_image()
        retR, color_image_R = captureR.get_color_image()

        if (num_bodiesL > 1) or (num_bodiesL == 0) or (num_bodiesR > 1) or (num_bodiesR == 0):
            continue
        if (not retL) or (not retR):
            continue
        out_file_json_L = "../pose_result/L/" + str(index) + ".json"
        out_file_json_R = "../pose_result/R/" + str(index) + ".json"
        with open(out_file_json_L, "w") as f:
            json.dump(jointsL, f)
        with open(out_file_json_R, "w") as f:
            json.dump(jointsR, f)
        # with open(out_file_json) as f:
        #     line = f.readline()
        #     data = json.loads(line)
        #     print(data[15])

        cv2.imwrite("../pose_result/L/" + str(index) + "_color_image.png", color_image_L)
        cv2.imwrite("../pose_result/R/" + str(index) + "_color_image.png", color_image_R)

        combined_image_L = color_image_L
        combined_image_R = color_image_R
        # Draw the skeletons
        combined_image_L = body_frame_L.draw_bodies(combined_image_L, pykinect.K4A_CALIBRATION_TYPE_COLOR)
        combined_image_R = body_frame_R.draw_bodies(combined_image_R, pykinect.K4A_CALIBRATION_TYPE_COLOR)
        cv2.imwrite("../pose_result/L/" + str(index) + "_combined_image.png", combined_image_L)
        cv2.imwrite("../pose_result/R/" + str(index) + "_combined_image.png", combined_image_R)

        # Overlay body segmentation on depth image
        cv2.imshow('combined_imageL', combined_image_L)
        cv2.imshow('combined_imageR', combined_image_R)
        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break
