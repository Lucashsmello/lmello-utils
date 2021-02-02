import cv2 as cv
import math
import numpy as np


def setFrame(vcap: cv.VideoCapture, fn: int):
    cur_fn = int(vcap.get(cv.CAP_PROP_POS_FRAMES))
    if(cur_fn > fn):
        if(fn-cur_fn > 25):
            print("WARNING: slow use of video [%d,%d]!" % (cur_fn, fn))
        vcap.set(cv.CAP_PROP_POS_FRAMES, fn)
    else:
        while(cur_fn < fn):
            vcap.grab()
            cur_fn += 1


def iterFrames(vcap: cv.VideoCapture):
    while(vcap.isOpened()):
        _, img = vcap.read()
        if(img is None):
            break
        yield img


def concatGridImages(imgs):
    n, h, w = imgs.shape
    ncols = int(n**0.5)
    nrows = math.ceil(n/ncols)
    ret = np.zeros((nrows*h, ncols*w))
    for i, img in enumerate(imgs):
        x1 = (i % ncols)*w
        x2 = x1+w
        y1 = (i // ncols)*h
        y2 = y1+h
        ret[y1:y2, x1:x2] = img
    return ret


def cropImage(img, crop):
    h, w, _ = img.shape
    return img[crop[0][1]:h-crop[1][1], crop[0][0]:w-crop[1][0]]


class AbortException(Exception):
    pass


def showWait(img, window_name='W', break_char='q', wait_time=1):
    cv.imshow(window_name, img)
    if cv.waitKey(wait_time) & 0xFF == ord(break_char):
        raise AbortException()
    return False


def redfilter3(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h = img[:, :, 0]
    l1=4
    l2=32
    mask = np.ones(h.shape, dtype=np.float)
    diff = 90 - abs(h.astype(np.int16) - 90)
    mask[diff > l1] = 1-(diff[diff > l1]-l1)/(l2-l1)
    mask[diff > l2] = 0
    

    img[:, :, 2] = img[:, :, 2] * mask
    img = cv.cvtColor(img, cv.COLOR_HSV2BGR)
    return img


def redfilter2(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = ((img[:, :, 0].astype(np.float) - 90)/90)**2
    # img[:, :, 1] = img[:, :, 1] * mask
    img[:, :, 2] = img[:, :, 2] * mask
    # showWait(mask, window_name='mask', wait_time=0)
    img = cv.cvtColor(img, cv.COLOR_HSV2BGR)
    return img


def redfilter(img, s=125, s2=255, v=25, v2=255, r=-6, r2=5):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_red = np.array([0, s, v])
    upper_red = np.array([r2, s2, v2])
    mask = cv.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([180+r, s, v])
    upper_red = np.array([180, s2, v2])
    mask2 = cv.inRange(hsv, lower_red, upper_red)
    mask = cv.bitwise_or(mask, mask2)
    res = cv.bitwise_and(img, img, mask=mask)
    return res
