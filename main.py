#!/usr/bin/python3

import numpy as np
import cv2 as cv
import multiprocessing
from dataclasses import dataclass


class Settings:
    DisplayOutput: bool
    Verbose: bool
    CaptureDevice: int

    def __init__(self):
        self.DisplayOutput = False
        self.Verbose = False
        self.CaptureDevice = 0
        self.EdgeDetectionType = 0
        self.EdgeThreshold = 100


class Video:

    def __init__(self, captureDevice: int = 0):
        self.__cap = cv.VideoCapture(captureDevice)

    def video(self):
        _, frame = self.__cap.read()
        # frame = cv.flip(frame, 1)
        return frame

    def edge_detection(self, s: Settings):
        frame_ = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_ = cv.blur(frame_, (1, 1))
        frame_ = cv.Canny(frame_, 100, 100 * 3, 3)
        return frame_


if __name__ == '__main__':
    s = Settings()

    # Set settings
    s.DisplayOutput = True
    s.Verbose = True
    s.CaptureDevice = 0
    s.EdgeDetectionType = 0
    s.EdgeThreshold = 100

    if s.Verbose == True:
        print("Test")

    cap = Video(s.CaptureDevice)


    while True:

        frame = cap.video()
        frame = cap.edge_detection(frame)

        cv.imshow("frame", frame)

        key = cv.waitKey(1)
        if key == 27:  # Key 'S'
            break
    cv.waitKey(0)
    cv.destroyAllWindows()
