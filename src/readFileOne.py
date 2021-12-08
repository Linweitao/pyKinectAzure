import sys
import cv2
import json

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":
    camera = "R"
    video_filename = "../data/output" + camera + ".mkv"

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    # Start playback
    playback = pykinect.start_playback(video_filename)

    playback_config = playback.get_record_configuration()
    # print(playback_config)

    playback_calibration = playback.get_calibration()

    # Start body tracker
    bodyTracker = pykinect.start_body_tracker(calibration=playback_calibration)

    cv2.namedWindow('combined_image', cv2.WINDOW_NORMAL)

    index = 0
    while playback.isOpened():
        index = index + 1
        # Get camera capture
        capture = playback.update()

        # Get body tracker frame
        body_frame = bodyTracker.update(capture=capture)

        # 获得关节点
        num_bodies, joints = body_frame.get_body_joints_CameraOfColor()
        if num_bodies > 1:
            continue
        if num_bodies == 0:
            continue
        out_file_json = "../pose_result/" + camera + "/" + str(index) + ".json"
        with open(out_file_json, "w") as f:
            json.dump(joints, f)

        # with open(out_file_json) as f:
        #     line = f.readline()
        #     data = json.loads(line)
        #     print(data[15])

        ret, color_image = capture.get_color_image()

        if not ret:
            continue

        cv2.imwrite("../pose_result/" + camera + "/" + str(index) + "_color_image.png", color_image)

        combined_image = color_image
        # Draw the skeletons
        combined_image = body_frame.draw_bodies(combined_image, pykinect.K4A_CALIBRATION_TYPE_COLOR)
        cv2.imwrite("../pose_result/" + camera + "/" + str(index) + "_combined_image.png", combined_image)

        # Overlay body segmentation on depth image
        cv2.imshow('combined_image', combined_image)

        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break
