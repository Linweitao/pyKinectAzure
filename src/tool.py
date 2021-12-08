import json

import numpy as np

# 坐标变换，已知A坐标系到B坐标系下的旋转矩阵R和平移矩阵T，求在A坐标系或B坐标系下的点在另一个坐标系下的坐标
# pointBelong为0时该点是A坐标系下的点，为1时该点是B坐标系下的点
from matplotlib import pyplot as plt

from pykinect_azure import pykinect, k4abt_body2D_t, k4abt_body_t, Body, Body2d


def Camera3dTo3dCoordinateConversion(point3d, R, T, pointBelong=0):
    RT = np.concatenate((R, T), axis=-1)
    Add = np.array([0, 0, 0, 1])
    RT = np.row_stack((RT, Add))
    point3d = np.append(point3d, 1)
    # print(RT)
    if pointBelong == 0:
        point3d_Conversion = np.dot(RT, point3d)
    elif pointBelong == 1:
        RT = np.linalg.inv(RT)
        point3d_Conversion = np.dot(RT, point3d)
    point3d_Conversion = np.delete(point3d_Conversion, -1)
    return point3d_Conversion


def Camera3dTo2dByK(point3d, K):
    z = point3d[2]
    point2d = np.dot(K, point3d) / z
    point2d = np.delete(point2d, -1)
    return point2d


def Camera3dTo2dByKinectSDK(videofilename, pts3d):
    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    # Start playback
    playback = pykinect.start_playback(videofilename)

    playback_config = playback.get_record_configuration()
    # print(playback_config)

    playback_calibration = playback.get_calibration()

    body2d_handle = k4abt_body2D_t()
    body_handle = k4abt_body_t()
    body = Body(body_handle)

    pts2d = []
    for pt3d in pts3d:
        body.joints[0].position.x = pt3d[0]
        body.joints[0].position.y = pt3d[1]
        body.joints[0].position.z = pt3d[2]
        for jointID, joint in enumerate(body.handle().skeleton.joints):
            body2d_handle.skeleton.joints2D[jointID].position = playback_calibration.convert_3d_to_2d(joint.position, 1,
                                                                                                      1)
        body2d = Body2d(body2d_handle)
        pts2d.append([body2d.joints[0].position.x, body2d.joints[0].position.y])
    return pts2d


def twoPoseVisCompare(out_file_json_L, out_file_json_R):
    p3do = []
    p3ds = []
    filename = 'camera_calibration'
    with open(filename) as file_obj:
        line = file_obj.readline()
        ccdata = json.loads(line)
        T = ccdata['T']
        R = ccdata['R']

    with open(out_file_json_L) as f:
        line = f.readline()
        dataL = json.loads(line)

    with open(out_file_json_R) as f:
        line = f.readline()
        dataR = json.loads(line)

    print("输出点")
    for jointL, jointR in zip(dataL, dataR):
        p3do.append(jointL["position3d"])
        point = Camera3dTo3dCoordinateConversion(jointR["position3d"], R, T, 1)
        p3ds.append(point)
        print(jointL["name"])
        print(jointL["confidence_level"], " ", jointR["confidence_level"])
        # if int(jointL["confidence_level"])>int(jointR["confidence_level"]):
        print(jointL["position3d"], " ", point)

    print("输出结束")
    p3ds = np.array(p3ds)
    p3do = np.array(p3do)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-2000, 2000)
    ax.set_ylim3d(-2000, 2000)
    ax.set_zlim3d(1000, 5000)

    connections = [[1, 0],
                   [2, 1],
                   [3, 2],
                   [4, 2],
                   [5, 4],
                   [6, 5],
                   [7, 6],
                   [8, 7],
                   [9, 8],
                   [10, 7],
                   [11, 2],
                   [12, 11],
                   [13, 12],
                   [14, 13],
                   [15, 14],
                   [16, 15],
                   [17, 14],
                   [18, 0],
                   [19, 18],
                   [20, 19],
                   [21, 20],
                   [22, 0],
                   [23, 22],
                   [24, 23],
                   [25, 24],
                   [26, 3],
                   [27, 26],
                   [28, 26],
                   [29, 26],
                   [30, 26],
                   [31, 26]]

    for _c in connections:
        ax.plot(xs=[p3do[_c[0], 0], p3do[_c[1], 0]], ys=[p3do[_c[0], 1], p3do[_c[1], 1]],
                zs=[p3do[_c[0], 2], p3do[_c[1], 2]], c='green')
        ax.plot(xs=[p3ds[_c[0], 0], p3ds[_c[1], 0]], ys=[p3ds[_c[0], 1], p3ds[_c[1], 1]],
                zs=[p3ds[_c[0], 2], p3ds[_c[1], 2]], c='red')

    ax.set_title('This figure can be rotated.')
    # uncomment to see the triangulated pose. This may cause a crash if youre also using cv.imshow() above.
    plt.show()

# out_file_json_L = "../pose_result/L/40.json"
# out_file_json_R = "../pose_result/R/40.json"
#
# twoPoseVisCompare(out_file_json_L,out_file_json_R)


# point3d = np.array([0, 0, 0])
# R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# T = np.array([[0], [0], [0]])
# print(Camera3dTo3dCoordinateConversion(point3d, R, T, 0))
