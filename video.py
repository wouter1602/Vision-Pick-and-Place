from settings import Settings
import cv2 as cv
import numpy as np


class Video:

    def __init__(self, s: Settings):
        if s.use_test_image:
            self._cap = cv.imread(s.test_image)
            self.frame = self._cap
        else:
            self._cap = cv.VideoCapture(s.capture_device)
            self._, self.frame = self._cap.read()

        self.grayscale = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.blur = cv.blur(self.frame, (1, 1))
        self.edge = cv.Canny(self.blur, s.edge_threshold_A, s.edge_threshold_B)
        self.lines = None
        self.video_lines = self.frame.copy()

    def _video(self, s: Settings):
        if s.use_test_image:
            self.frame = self._cap
        else:
            self._, self.frame = self._cap.read()

    def video(self, s: Settings):
        self._video(s)
        return self.frame

    def edge_detection(self, s: Settings):
        self._video(s)
        self.grayscale = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        # self.blur = cv.blur(self.frame, (1, 1))

        # self.edge = cv.Canny(self.blur, 100, 100 * 3, 3)
        self.edge = cv.Canny(self.grayscale, s.edge_threshold_A, s.edge_threshold_B)

    def detect_lines(self, s: Settings):
        self.lines = cv.HoughLinesP(self.edge, 1, np.pi / 180, 60, np.array([]), 50, 5)

    def draw_lines(self, s: Settings):
        self.video_lines = self.frame.copy()
        for line in self.lines:
            for x1, y1, x2, y2 in line:
                cv.line(self.video_lines, (x1, y1), (x2, y2), (255, 0, 0), 3)

    def __del__(self) -> int:
        # TODO: Create deconstruct
        return 0
