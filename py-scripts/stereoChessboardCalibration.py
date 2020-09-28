import numpy as np
import cv2
import cv2.aruco as aruco
import time
import datetime
from tempfile import TemporaryFile
import json

# CONFIGURATION PARAMETERS

# The number of images to capture before beginning calibration
numImagesRequired = 20
# The dimension of a single square on the checkerboard in METERS
checkerboardDimension = 0.027 # This equates to 27 millimeter wide squares
# The number of inside corners on the width (long axis) of the checkerboard
checkerboardWidth = 9
# The number of inside corners on the height (short axis) of the checkerboard
checkerboardHeight = 6

# Initialize some persistent state variables
calibration = None
allLeftCorners = []
allRightCorners = []
lastTime = 0

# Check to see if an existing calibration exists
calibrated = False
try:
    calibration = np.load("cameraCalibration_cv2.npz")
    calibrated = True
except:
    print("No Calibration file found...")

undistortMap = None
if(calibrated):
    leftUndistortMap = [None, None]
    leftUndistortMap[0], leftUndistortMap[1] = cv2.initUndistortRectifyMap(calibration['leftCameraMatrix'], calibration['leftDistCoeffs'], calibration['R1'], calibration['P1'], (640,480), cv2.CV_32FC1 )
    rightUndistortMap = [None, None]
    rightUndistortMap[0], rightUndistortMap[1] = cv2.initUndistortRectifyMap(calibration['rightCameraMatrix'], calibration['rightDistCoeffs'], calibration['R2'], calibration['P2'], (640,480), cv2.CV_32FC1 )
    undistortMap = (leftUndistortMap, rightUndistortMap)

# Chessboard parameters
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ...., (checkerboardWidth, checkerboardHeight,0)
objpp = np.zeros((checkerboardHeight*checkerboardWidth,3), np.float32)
objpp[:,:2] = np.mgrid[0:checkerboardWidth,0:checkerboardHeight].T.reshape(-1,2)
objpp = objpp * checkerboardDimension # Set the Object Points to be in real coordinates
objpp = np.asarray([objpp])
objp = np.copy(objpp)
for x in range(numImagesRequired-1):
    objp = np.concatenate((objp, objpp), axis=0)

# Termination Criteria for the subpixel corner refinement
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Begin webcam capture
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_EXPOSURE, -7)

combinedFrames = None
while(not (cv2.waitKey(1) & 0xFF == ord('q'))):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if(ret and frame is not None):

        leftFrame = frame[:, :int(frame.shape[1]/2)]
        rightFrame = frame[:, int(frame.shape[1]/2):]

        if(calibrated):
            combinedFrames = np.hstack((cv2.remap(leftFrame,  undistortMap[0][0], undistortMap[0][1], cv2.INTER_LINEAR),
                                        cv2.remap(rightFrame, undistortMap[1][0], undistortMap[1][1], cv2.INTER_LINEAR)))

            # Draw Epipolar Lines
            for y in range(int(combinedFrames.shape[0]*0.025)):
                cv2.line(combinedFrames, (0, y*40), (int(combinedFrames.shape[1]*2), y*40), 255, 1)

        else:
            if(calibration is None):
                # Detect the Chessboard Corners in the Left Image
                gray = cv2.cvtColor(leftFrame, cv2.COLOR_BGR2GRAY)
                leftDetected, corners = cv2.findChessboardCorners(gray, (checkerboardWidth,checkerboardHeight), None, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK)
                if leftDetected:
                    leftCorners = cv2.cornerSubPix(gray, corners,(checkerboardWidth,checkerboardHeight),(-1,-1),criteria)
                    cv2.drawChessboardCorners(leftFrame, (checkerboardWidth,checkerboardHeight), leftCorners, ret)

                # Detect the Chessboard Corners in the Right Image
                gray = cv2.cvtColor(rightFrame, cv2.COLOR_BGR2GRAY)
                rightDetected, corners = cv2.findChessboardCorners(gray, (checkerboardWidth,checkerboardHeight), None, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK)
                if rightDetected:
                    rightCorners = cv2.cornerSubPix(gray, corners,(checkerboardWidth,checkerboardHeight),(-1,-1),criteria)
                    cv2.drawChessboardCorners(rightFrame, (checkerboardWidth,checkerboardHeight), rightCorners, ret)

                # Add the detected points to our running arrays when the board is detected in both cameras
                if(leftDetected and rightDetected and time.time() - lastTime > 1):
                    allLeftCorners.append(leftCorners)
                    allRightCorners.append(rightCorners)
                    lastTime = time.time()
                    print("Added Snapshot to array of points")

                # Once we have all the data we need, begin calibrating!!!
                if(len(allLeftCorners)==numImagesRequired and not calibrated):
                    print("Beginning Left Camera Calibration")
                    leftValid, leftCameraMatrix, leftDistCoeffs, leftRvecs, leftTvecs = cv2.calibrateCamera(objp, allLeftCorners, (leftFrame.shape[0], leftFrame.shape[1]), None, None)
                    if(leftValid):
                        print("Left Camera Successfully Calibrated!!")
                        print("Left Camera Matrix:")
                        print(leftCameraMatrix)
                        print("Left Camera Distortion Coefficients:")
                        print(leftDistCoeffs)
                    print("Beginning Right Camera Calibration")
                    rightValid, rightCameraMatrix, rightDistCoeffs, rightRvecs, rightTvecs = cv2.calibrateCamera(objp, allRightCorners, (leftFrame.shape[0], leftFrame.shape[1]), None, None)
                    if(rightValid):
                        print("Right Camera Successfully Calibrated!!")
                        print("Right Camera Matrix:")
                        print(rightCameraMatrix)
                        print("Right Camera Distortion Coefficients:")
                        print(rightDistCoeffs)
                    if(leftValid and rightValid):
                        print("WE DID IT, HOORAY!   Now beginning stereo calibration...")
                        valid, leftCameraMatrix, leftDistCoeffs, rightCameraMatrix, rightDistCoeffs, leftToRightRot, leftToRightTrans, essentialMat, fundamentalMat = (
                            cv2.stereoCalibrate(objp, allLeftCorners, allRightCorners, leftCameraMatrix, leftDistCoeffs, rightCameraMatrix, rightDistCoeffs, (leftFrame.shape[0], leftFrame.shape[1])))

                        if(valid):
                            # Construct the stereo-rectified parameters for display
                            R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(leftCameraMatrix,  leftDistCoeffs, 
                                                                                              rightCameraMatrix, rightDistCoeffs, 
                                                                                             (leftFrame.shape[0], leftFrame.shape[1]), 
                                                                                              leftToRightRot, leftToRightTrans)

                            leftUndistortMap = [None, None]
                            leftUndistortMap[0], leftUndistortMap[1] = cv2.initUndistortRectifyMap(leftCameraMatrix, leftDistCoeffs, 
                                                                                                   R1, P1, (leftFrame.shape[1], leftFrame.shape[0]), cv2.CV_32FC1)
                            rightUndistortMap = [None, None]
                            rightUndistortMap[0], rightUndistortMap[1] = cv2.initUndistortRectifyMap(rightCameraMatrix, rightDistCoeffs, 
                                                                                                     R2, P2, (leftFrame.shape[1], leftFrame.shape[0]), cv2.CV_32FC1)
                            undistortMap = (leftUndistortMap, rightUndistortMap)

                            print("Stereo Calibration Completed!")
                            print("Left to Right Rotation Matrix:")
                            print(leftToRightRot)
                            print("Left to Right Translation:")
                            print(leftToRightTrans)
                            print("Essential Matrix:")
                            print(essentialMat)
                            print("Fundamental Matrix:")
                            print(fundamentalMat)

                            np.savez("cameraCalibration_cv2.npz",
                                leftCameraMatrix=leftCameraMatrix,
                                rightCameraMatrix=rightCameraMatrix,
                                leftDistCoeffs=leftDistCoeffs,
                                rightDistCoeffs=rightDistCoeffs,
                                leftToRightTrans=leftToRightTrans,
                                leftToRightRot=leftToRightRot,
                                R1=R1,
                                R2=R2,
                                P1=P1,
                                P2=P2,
                                baseline=float(leftToRightTrans[0]*-1.0)
                            )
                            calibrated = True

            combinedFrames = np.hstack((leftFrame, rightFrame))

        #Image
        if(combinedFrames is not None):
            cv2.imshow('Combined Frames', combinedFrames)

# When everything is done, release the capture
cv2.destroyAllWindows()
cap.release()
