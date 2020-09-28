import os
import numpy as np
import cv2
import math
import time
import abc
import typing
from polyHelpers import *

def cachedArray(func):
    def inner(self, height, width):
        if(hasattr(self, "_cache") is not True):
            self._cache = {}
        cachedValue = self._cache.get(func.__name__)
        if(cachedValue is None or cachedValue.shape != (height, width)):
            self._cache[func.__name__] = func(self, height, width)
        return self._cache[func.__name__]
    return inner

class Borg:
    
    _shared_state = {}
    
    def __init__(self):
        self.__dict__ = self._shared_state
        if(getattr(self, "_initialized", False) is False):
            self.initialize()
            self._initialized = True
        return
    
    def initialize(self):
        return

class CalibrationHelpers(Borg):
    
    _shared_state = {}
    
    def __init__(self):
        Borg.__init__(self)
        self.continuum = self._continuum()
        return
    
    @cachedArray
    def allWhite(self, height, width):
        return np.ones((height, width), dtype=np.uint8) * 100
    
    @cachedArray
    def allDark(self, height, width):
        return np.zeros((height, width), dtype=np.uint8)
    
    def _continuum(self):
        c = np.arange(0, 256, dtype=np.uint8)
        c = np.bitwise_xor(c, c//2) # Binary to Gray
        return c
    
    @cachedArray
    def widthContinuum(self, height, width):
        wc = self.allDark(height, width)
        c = self.continuum
        wc[:, : int(width / 2)] = cv2.resize(c[None, :], (int(width / 2), height), interpolation=cv2.INTER_NEAREST)
        wc[:, int(width / 2) :] = wc[:, : int(width / 2)]
        return wc
        
    @cachedArray
    def heightContinuum(self, height, width):
        return cv2.resize(self.continuum[:, None], (width, height), interpolation=cv2.INTER_NEAREST)
        
    @cachedArray
    def widthBits(self, height, width):
        wc = self.widthContinuum(height, width)
        return np.unpackbits(wc[: , :, None].astype(np.uint8), axis=-1)
        
    @cachedArray
    def heightBits(self, height, width):
        hc = self.heightContinuum(height, width)
        return np.unpackbits(hc[:, :, None].astype(np.uint8), axis=-1)
        
    @staticmethod
    def calibration2GLSL(cal):
        glslStrs = []
        for key, coeffs in cal.items():
            glslStr = f"float[] {key} = float[{len(coeffs)}] ("
            glslStr += ", ".join(map(str, coeffs))
            glslStr += ");"
            glslStrs.append(glslStr)
        return "\n".join(glslStrs)

class Camera(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def readCapture(self) -> typing.Tuple[bool, np.ndarray]:
        return
        
    @abc.abstractmethod
    def release(self):
        return
        
    @property
    @abc.abstractmethod
    def resolution(self) -> typing.Tuple[int, int]:
        return
        
    @property
    @abc.abstractmethod
    def calibration(self) -> dict:
        return
        
    def readNewFrame(self, waitTime=0.1, tryCount=10):
        for _ in range(tryCount):
            ret, frame = self.readCapture()
            if(ret is True):
                return frame
            time.sleep(waitTime)
        camera.release()
        raise Exception('cannot read frame')
        return None

class T265Camera(Camera): #can be potentially refactored to generic realsense camera however everything in intelutils is probably hardcoded for t265
    
    def __init__(self):
        import pyrealsense2 as rs2
        import intelutils
        self._cap = intelutils.intelCamThread(frame_callback = lambda frame: None)
        self._cap.start()
        self._frameWidth = 848 * 2
        self._frameHeight = 800
        return
        
    def readCapture(self):
        return self._cap.read()
        
    def release(self):
        self._cap.kill()
        return
        
    @property
    def calibration(self):
        return np.load("./cameraCalibration_rs.npz", ) #TODO consider read always vs init
        
    def readNewFrame(self, waitTime=0.1, tryCount=10):
        self.readCapture() #reseting newFrame flag in intelutils
        return Camera.readNewFrame(self, waitTime, tryCount)
        
    @property
    def resolution(self):
        return (self._frameHeight, self._frameWidth)

class CV2Camera(Camera):
    
    def __init__(self, index, frameHeight, frameWidth):
        self._frameHeight = frameHeight
        self._frameWidth = frameWidth
        self._cap = cv2.VideoCapture(index)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH , self._frameWidth)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._frameHeight)
        self.readNewFrame() #first frame not reliable
        return
        
    def readCapture(self):
        return self._cap.read()
        
    def release(self):
        self._cap.release()
        return
        
    @property
    def resolution(self):
        return (self._frameHeight, self._frameWidth)
      
    @property
    def calibration(self):
        return np.load("./cameraCalibration_cv2.npz", ) #TODO consider read always vs init
        
    def readNewFrame(self, waitTime=0.1, tryCount=10):
        return cv2.cvtColor(Camera.readNewFrame(self, waitTime, tryCount), cv2.COLOR_BGR2GRAY)

class CalibrationManager(Borg):

    _shared_state = {}

    def __init__(self):
        Borg.__init__(self)
        return
        
    def initialize(self):
        self.camera = None
        self.windowName = None
        self.displayResolution = None
        self.helpers = CalibrationHelpers()
        return
        
    def createFullscreenWindow(self, offsetX=1920, offsetY=0, name="Viewport", destroyPrev=True):
        if(destroyPrev is True and self.windowName is not None):
            cv2.destroyWindow(self.windowName)
        self.windowName = name
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.windowName, offsetX, offsetY)
        cv2.setWindowProperty(self.windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        return
        
    def setActiveCamera(self, camera):
        if(self.camera is not None):
            self.camera.release()
        self.camera = camera
        return
        
    def setDisplayResolution(self, pVertical, pHorizontal):
        self.displayResolution = (pVertical, pHorizontal)
        return
        
    def createMonitorMaskRoutine(self, threshold=53, displayTimeMs=200):
        aw = self.helpers.allWhite(*self.displayResolution)
        ad = self.helpers.allDark(*self.displayResolution)
        cv2.imshow(self.windowName, aw)
        cv2.waitKey(displayTimeMs)
        frame = self.camera.readNewFrame()
        cv2.imshow(self.windowName, ad)
        cv2.waitKey(displayTimeMs)
        darkFrame = self.camera.readNewFrame()
        return self.createMask(frame, darkFrame, threshold)
        
    def measureBitsRoutine(self, bits, mask, invert=False, brightness=127, threshold=1, displayTimeMs=250, colorOverride = None):
        displayedBuffer = bits[:, :, 0] * brightness
        darkFrameBuffer = None
        measuredBits = np.ones((self.camera.resolution) + (8, ), dtype=np.uint8)
        lastResult = np.full(self.camera.resolution, invert, dtype=np.uint8)
        for i in range(15):
            bitIndex = (i + 1) // 2
            cv2.imshow(self.windowName, displayedBuffer if colorOverride is None else cv2.merge((displayedBuffer * colorOverride[0], displayedBuffer * colorOverride[1], displayedBuffer * colorOverride[2])))
            cv2.waitKey(displayTimeMs)
            frame = self.camera.readNewFrame()
            if i % 2 is 0:
                darkFrameBuffer = frame.copy()
                displayedBuffer = (1 - bits[:, :, bitIndex]) * brightness
            else:
                bitmask = self.createMask(frame, darkFrameBuffer, 1)
                lastResult = bitmask == lastResult # xor with last bitmask - Grey -> binary
                measuredBits[:, :, bitIndex - 1] = lastResult
                displayedBuffer = bits[:, :, bitIndex] * brightness
        return np.packbits(measuredBits, axis=-1)[:, :, 0] * mask
        
    def createMask(self, frame, darkFrame, threshold):
        mask = cv2.threshold(cv2.subtract(frame, darkFrame), thresh=threshold, maxval=1, type=cv2.THRESH_BINARY)[1]
        return mask
        
    def calibrateGreycodes(self, widthData, heightData, calibration=None, fisheye=True):
        rawData    = np.zeros((widthData.shape[0], widthData.shape[1], 3), dtype=np.uint8)
        rawData[..., 2] = widthData; rawData[..., 1] = heightData
        leftData   = rawData [:, : int(rawData.shape[1] / 2)  ]
        rightData  = rawData [:,   int(rawData.shape[1] / 2) :]

        if(calibration is None):
            calibration = self.camera.calibration
        leftCoeffs = calcCoeffs(leftData , calibration['leftCameraMatrix' ], calibration['leftDistCoeffs' ], calibration['R1'], fisheye)
        rightCoeffs = calcCoeffs(rightData, calibration['rightCameraMatrix'], calibration['rightDistCoeffs'], calibration['R2'], fisheye)
        
        return {
            'left_uv_to_rect_x' : leftCoeffs[0].flatten().tolist(),  'left_uv_to_rect_y': leftCoeffs[1].flatten().tolist(),
            'right_uv_to_rect_x': rightCoeffs[0].flatten().tolist(), 'right_uv_to_rect_y': rightCoeffs[1].flatten().tolist()
        }

if __name__ == '__main__':
    """OFFLINE MODE - from files, no devices
    import sys
    cm = CalibrationManager()
    mbw = cv2.imread("./WidthCalibration.png", cv2.IMREAD_GRAYSCALE)
    mbh = cv2.imread("./HeightCalibration.png", cv2.IMREAD_GRAYSCALE)
    cal = cm.calibrateGreycodes(mbw, mbh, np.load("./cameraCalibration_cv2.npz", ), False)
    print(cal)
    print(CalibrationHelpers.calibration2GLSL(cal))
    sys.exit(0)
    """
    
    ch = CalibrationHelpers()
    cm = CalibrationManager()
    cm.setDisplayResolution(1920, 1080)
    cm.createFullscreenWindow(1920, 0)
    cv2.imshow(cm.windowName, ch.allWhite(*cm.displayResolution))
    camera = CV2Camera(1, 720, 2560)
    fisheye = False
    #camera = T265Camera()
    #fisheye = True #move to camera properties? need it also for offline (no camera)
    cv2.waitKey(200)
    cm.setActiveCamera(camera)
    mask = cm.createMonitorMaskRoutine(150, 1000)
    cv2.imshow("res", mask * 100) #binary mask
    cv2.waitKey(200)
    widthBits = ch.widthBits(*cm.displayResolution)
    mbw = cm.measureBitsRoutine(widthBits, mask)
    cv2.imshow("res", cv2.applyColorMap(mbw, cv2.COLORMAP_JET))
    cv2.imwrite("./WidthCalibration.png", mbw)
    """ SUBPIXEL TEST
    widthBits = ch.widthBits(*cm.displayResolution)
    mbg = cm.measureBitsRoutine(widthBits, mask, brightness=127, threshold=1, displayTimeMs=200, colorOverride = (0,1,0))
    cv2.imshow("res", cv2.applyColorMap(mbg, cv2.COLORMAP_JET))
    #cv2.waitKey(0)
    mbb = cm.measureBitsRoutine(widthBits, mask, brightness=127, threshold=1, displayTimeMs=200, colorOverride = (1,0,0))
    cv2.imshow("res", cv2.applyColorMap(mbb, cv2.COLORMAP_JET))
    #cv2.waitKey(0)
    mbr = cm.measureBitsRoutine(widthBits, mask, brightness=127, threshold=1, displayTimeMs=200, colorOverride = (0,0,1))
    cv2.imshow("res", cv2.applyColorMap(mbr, cv2.COLORMAP_JET))
    #cv2.waitKey(0)
    merged = cv2.merge((mbb, mbg, mbr))
    cv2.imshow("res", merged)
    cv2.waitKey(0)
    """
    heightBits = ch.heightBits(*cm.displayResolution)
    mbh = cm.measureBitsRoutine(heightBits, mask, True)
    cv2.imshow("res", cv2.applyColorMap(mbh, cv2.COLORMAP_JET))
    cv2.imwrite("./HeightCalibration.png", mbh)
    camera.release()
    cv2.waitKey(0)
    cal = cm.calibrateGreycodes(mbw, mbh, None, fisheye)
    print(cal)
    print(CalibrationHelpers.calibration2GLSL(cal))