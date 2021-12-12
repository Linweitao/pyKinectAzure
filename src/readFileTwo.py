import os
import shutil
import sys
import cv2
import json

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":
    person_name = input("person name: ")
    video_filenameL = "../data/"+person_name+"/outputL.mkv"
    video_filenameR = "../data/"+person_name+"/outputR.mkv"
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

    out_file_json = "../pose_result/" + person_name
    if not os.path.exists(out_file_json):
        os.mkdir(out_file_json)
    else:
        shutil.rmtree(out_file_json)
        os.mkdir(out_file_json)
    out_file_L = "../pose_result/" + person_name + "/L/"
    out_file_R = "../pose_result/" + person_name + "/R/"
    if not os.path.exists(out_file_L):
        os.mkdir(out_file_L)
    else:
        shutil.rmtree(out_file_L)
        os.mkdir(out_file_L)

    if not os.path.exists(out_file_R):
        os.mkdir(out_file_R)
    else:
        shutil.rmtree(out_file_R)
        os.mkdir(out_file_R)

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
        # 人数超过一个人或者没有识别到人，那么直接跳过
        if (num_bodiesL > 1) or (num_bodiesL == 0) or (num_bodiesR > 1) or (num_bodiesR == 0):
            print("numbodiesL: ", num_bodiesL)
            print("numbodiesR: ", num_bodiesR)
            continue
        if (not retL) or (not retR):
            continue



        out_file_json_L = out_file_L + str(index) + ".json"
        out_file_json_R = out_file_R + str(index) + ".json"
        with open(out_file_json_L, "w") as f:
            json.dump(jointsL, f)
        with open(out_file_json_R, "w") as f:
            json.dump(jointsR, f)
        # with open(out_file_json) as f:
        #     line = f.readline()
        #     data = json.loads(line)
        #     print(data[15])

        cv2.imwrite(out_file_L + str(index) + "_color_image.png", color_image_L)
        cv2.imwrite(out_file_R + str(index) + "_color_image.png", color_image_R)

        combined_image_L = color_image_L
        combined_image_R = color_image_R
        # Draw the skeletons
        combined_image_L = body_frame_L.draw_bodies(combined_image_L, pykinect.K4A_CALIBRATION_TYPE_COLOR)
        combined_image_R = body_frame_R.draw_bodies(combined_image_R, pykinect.K4A_CALIBRATION_TYPE_COLOR)
        cv2.imwrite(out_file_L + str(index) + "_combined_image.png", combined_image_L)
        cv2.imwrite(out_file_R + str(index) + "_combined_image.png", combined_image_R)

        # Overlay body segmentation on depth image
        cv2.imshow('combined_imageL', combined_image_L)
        cv2.imshow('combined_imageR', combined_image_R)
        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break
