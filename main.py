#!/usr/bin/python3

import numpy as np
import cv2 as cv
import multiprocessing
from dataclasses import dataclass
import socket


class Settings:
    display_output: bool
    verbose: bool
    capture_device: int
    edge_detection_type: int
    edge_threshold: int
    TCP_IP: str
    TCP_PORT: int
    use_test_image: bool
    test_image: str

    def __init__(self):
        self.display_output = False
        self.verbose = False
        self.capture_device = 0
        self.edge_detection_type = 0
        self.edge_threshold = 100
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5000
        self.use_test_image = False
        self.test_image = "Test_Img.jpg"


class Video:

    def __init__(self, s: Settings):
        if s.use_test_image:
            self.__cap = cv.imread("Test_Img.jpg")

        else:
            self.__cap = cv.VideoCapture(s.capture_device)

        self._, self.frame = self.__cap.read()
        self.grayscale = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.blur = cv.blur(self.frame, (1, 1))
        self.edge = cv.Canny(self.blur, 100, 100 * 3, 3)

    def __video(self):
        self._, self.frame = self.__cap.read()

    def video(self):
        self.__video()
        return self.frame

    def edge_detection(self, s: Settings):
        self.__video()
        self.grayscale = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.blur = cv.blur(self.frame, (1, 1))

        self.edge = cv.Canny(self.blur, 100, 100 * 3, 3)
        return self.edge


def main() -> None:
    s = Settings()

    # Set settings
    s.display_output = True
    s.verbose = True
    s.use_test_image = False

    s.capture_device = 0
    s.edge_detection_type = 0
    s.edge_threshold = 100

    if s.verbose:
        print("Test")

    cap = Video(s)

    while True:

        edge = cap.edge_detection(s)

        if s.verbose:
            cv.imshow("Frame", cap.frame)
            cv.imshow("Grayscale", cap.grayscale)
            cv.imshow("Blur", cap.blur)
            cv.imshow("Edges", cap.edge)

        key = cv.waitKey(1)
        if key == 27:  # Key 'S'
            break
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
