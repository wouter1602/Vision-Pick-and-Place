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
        self.canny = cv.Canny(self.blur, s.edge_threshold_A, s.edge_threshold_B)
        self.contours = None
        self.hierarchy = None
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

    def _grayscale(self):
        self.grayscale = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

    def edge_canny(self, s: Settings):
        self._video(s)
        self._grayscale()

        self.canny = cv.Canny(self.grayscale, s.edge_threshold_A, s.edge_threshold_B)

    def edge_contour(self, s: Settings):
        self._video(s)
        self._grayscale()

        ret, self.thrash = cv.threshold(self.grayscale, s.contour_threshold_A, s.contour_threshold_B, cv.CHAIN_APPROX_NONE)
        self.contours, self.hierarchy = cv.findContours(self.thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    def draw_contour(self, s: Settings):
        self.video_lines = self.frame.copy()
        for contour in self.contours:
            approx = cv.approxPolyDP(contour, 0.01* cv.arcLength(contour, True), True)
            cv.drawContours(self.video_lines, [approx], 0, (0, 0, 0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            if len(approx) == 3:
                cv.putText(self.video_lines, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 4:
                x, y, w, h = cv.boundingRect(approx)
                aspect_ratio = float(w) / h
                if s.verbose:
                    print("Aspect ratio", aspect_ratio)
                if 0.95 <= aspect_ratio < 1.05:
                    cv.putText(self.video_lines, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                else:
                    cv.putText(self.video_lines, "Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 5:
                cv.putText(self.video_lines, "Pentagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 10:
                cv.putText(self.video_lines, "Star", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            else:
                cv.putText(self.video_lines, "Circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    def detect_lines(self, s: Settings):
        return cv.HoughLinesP(self.canny, 1, np.pi / 180, 60, np.array([]), 50, 5)

    def draw_lines(self, s: Settings, lines):
        self.video_lines = self.frame.copy()
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(self.video_lines, (x1, y1), (x2, y2), (255, 0, 0), 3)

    def detect_objects(self, s: Settings):
        if s.edge_detection_type:
            self.edge_contour(s)
            self.draw_contour(s)
        else:
            self.edge_canny(s)
            # self.draw_lines(s, self.detect_lines(s))

    def __del__(self) -> int:
        # TODO: Create deconstruct
        return 0
