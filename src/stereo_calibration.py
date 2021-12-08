import os

import cv2 as cv
import glob
import numpy as np
import json
import easygui


def calibrate_camera(images_folder):
    images_names = sorted(glob.glob(images_folder))
    images = []
    for imname in images_names:
        im = cv.imread(imname, 1)
        images.append(im)

    # criteria used by checkerboard pattern detector.
    # Change this if the code can't find the checkerboard
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    rows = 6  # number of checkerboard rows.
    columns = 9  # number of checkerboard columns.
    world_scaling = 26  # change this to the real world square size. Or not.
    accuracy = 3  # accuracy of key point (pixel)

    # coordinates of squares in the checkerboard world space
    objp = np.zeros((rows * columns, 3), np.float32)
    objp[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
    objp = world_scaling * objp

    # frame dimensions. Frames should be the same size.
    width = images[0].shape[1]
    height = images[0].shape[0]

    # Pixel coordinates of checkerboards
    imgpoints = []  # 2d points in image plane.

    # coordinates of the checkerboard in checkerboard world space.
    objpoints = []  # 3d point in real world space

    for frame in images:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # find the checkerboard
        ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)

        if ret:
            # Convolution size used to improve corner detection. Don't make this too large.
            conv_size = (accuracy, accuracy)

            # opencv can attempt to improve the checkerboard coordinates
            corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
            cv.drawChessboardCorners(frame, (rows, columns), corners, ret)
            cv.imshow('img', frame)
            k = cv.waitKey(10)

            objpoints.append(objp)
            imgpoints.append(corners)

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
    print('rmse:', ret)
    print('camera matrix:\n', mtx)
    print('distortion coeffs:', dist)

    return mtx, dist


def stereo_calibrate(mtx1, dist1, mtx2, dist2, frames_folder):
    # read the synched frames
    c1_images_names = os.listdir(frames_folder + "/L/")
    c2_images_names = os.listdir(frames_folder + "/R/")
    c1_images_names = sorted(c1_images_names)
    c2_images_names = sorted(c2_images_names)
    c1_images = []
    c2_images = []
    for im1, im2 in zip(c1_images_names, c2_images_names):
        _im = cv.imread(frames_folder + "/L/" + im1, 1)
        c1_images.append(_im)

        _im = cv.imread(frames_folder + "/R/" + im2, 1)
        c2_images.append(_im)

    # change this if stereo calibration not good.
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

    rows = 6  # number of checkerboard rows.
    columns = 9  # number of checkerboard columns.
    world_scaling = 26.  # change this to the real world square size. Or not.
    accuracy = 4  # accuracy of key point (pixel)
    # coordinates of squares in the checkerboard world space
    objp = np.zeros((rows * columns, 3), np.float32)
    objp[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
    objp = world_scaling * objp

    # frame dimensions. Frames should be the same size.
    width = c1_images[0].shape[1]
    height = c1_images[0].shape[0]

    # Pixel coordinates of checkerboards
    imgpoints_left = []  # 2d points in image plane.
    imgpoints_right = []

    # coordinates of the checkerboard in checkerboard world space.
    objpoints = []  # 3d point in real world space

    for frame1, frame2 in zip(c1_images, c2_images):
        gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        c_ret1, corners1 = cv.findChessboardCorners(gray1, (rows, columns), None)
        c_ret2, corners2 = cv.findChessboardCorners(gray2, (rows, columns), None)

        if c_ret1 == True and c_ret2 == True:
            corners1 = cv.cornerSubPix(gray1, corners1, (accuracy, accuracy), (-1, -1), criteria)
            corners2 = cv.cornerSubPix(gray2, corners2, (accuracy, accuracy), (-1, -1), criteria)

            cv.drawChessboardCorners(frame1, (rows, columns), corners1, c_ret1)
            # cv.imshow('img', frame1)

            cv.drawChessboardCorners(frame2, (rows, columns), corners2, c_ret2)
            # cv.imshow('img2', frame2)
            # k = cv.waitKey(100)

            objpoints.append(objp)
            imgpoints_left.append(corners1)
            imgpoints_right.append(corners2)

    # stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
    stereocalibration_flags = cv.CALIB_USE_INTRINSIC_GUESS
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(objpoints, imgpoints_left, imgpoints_right,
                                                                 mtx1, dist1,
                                                                 mtx2, dist2, (width, height),
                                                                 criteria=criteria,
                                                                 flags=stereocalibration_flags)

    print("stereo rmse: ")
    print(ret)

    return R, T


Lpath = easygui.diropenbox('请选择左相机图像文件夹')  # choose folder
Lpath = '/'.join(Lpath.split('\\'))  # path convert for windows
Rpath = easygui.diropenbox('请选择右相机图像文件夹')
Rpath = '/'.join(Rpath.split('\\'))  # path convert for windows
mtx1, dist1 = calibrate_camera(images_folder=Lpath+'/*')
print("calibrate_cameraL end")
mtx2, dist2 = calibrate_camera(images_folder=Rpath+'/*')
print("calibrate_cameraR end")

# 从kinect获得的内参
# mtx1 = np.array(
#     [[915.3875732421875, 0.0, 959.9261474609375], [0.0, 914.9352416992188, 549.2899169921875], [0.0, 0.0, 1.0]])
# mtx2 = np.array(
#     [[913.8087768554688, 0.0, 952.2326049804688], [0.0, 913.4713745117188, 555.8916015625], [0.0, 0.0, 1.0]])
# dist1 = np.array([[0.2999665141105652, -2.8757076263427734, 0.0011606672778725624, -0.0004085998807568103,
#                    1.883712649345398, 0.17953889071941376, -2.671276569366455, 1.7857621908187866]])
# dist2 = np.array([[0.06096123158931732, -2.186087131500244, 0.0010949646821245551, -0.0006320280954241753,
#                    1.4191652536392212, -0.053511157631874084, -2.003505229949951, 1.3374310731887817]])

# Steropath = easygui.diropenbox('请选择融合图像文件夹')
# Steropath = '/'.join(Steropath.split('\\'))  # path convert
Steropath = "../calibrationPic"
R, T = stereo_calibrate(mtx1, dist1, mtx2, dist2, Steropath)
print("stereo_calibrate end")
print(R)
print(T)
camera_calibration_data = {"T": T.tolist(), "R": R.tolist()}
filename = 'camera_calibration'
with open(filename, 'w') as file_obj:
    json.dump(camera_calibration_data, file_obj)

'''''
with open(filename, 'w') as file_obj:
    # json.dump(mtx1.tolist(), file_obj)
    # json.dump(mtx2.tolist(), file_obj)
    json.dump(T.tolist(), file_obj)
    # json.dump(R.tolist(), file_obj)

filename = 'camera_calibration_R'
with open(filename, 'w') as file_obj:
    # json.dump(mtx1.tolist(), file_obj)
    # json.dump(mtx2.tolist(), file_obj)
    # json.dump(T.tolist(), file_obj)
    json.dump(R.tolist(), file_obj)

filename = 'camera_calibration_mtx1'
with open(filename, 'w') as file_obj:
    json.dump(mtx1.tolist(), file_obj)
    # json.dump(mtx2.tolist(), file_obj)
    # json.dump(T.tolist(), file_obj)
    # json.dump(R.tolist(), file_obj)

filename = 'camera_calibration_mtx2'
with open(filename, 'w') as file_obj:
    # json.dump(mtx1.tolist(), file_obj)
    json.dump(mtx2.tolist(), file_obj)
    # json.dump(T.tolist(), file_obj)
    # json.dump(R.tolist(), file_obj)
'''
