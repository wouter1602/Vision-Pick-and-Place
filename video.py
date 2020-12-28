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
        self.canny = cv.Canny(self.blur, s.canny_threshold_A, s.canny_threshold_B)
        self.lines = None
        self.thrash = None
        self.video_output = self.frame.copy()

    def _video(self, s: Settings):
        if s.use_test_image:
            self.frame = self._cap
        else:
            self._, self.frame = self._cap.read()

    def _grayscale(self):
        self.grayscale = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

    def _edge_canny(self, s: Settings):
        self._video(s)
        self._grayscale()

        self.canny = cv.Canny(self.grayscale, s.canny_threshold_A, s.canny_threshold_B)

    def _threshold(self, s):
        self._video(s)
        self._grayscale()

        ret, self.thrash = cv.threshold(self.grayscale, s.contour_threshold_A, s.contour_threshold_B,
                                        cv.CHAIN_APPROX_NONE)

    def _edge_contour(self, s: Settings, frame):
        contours, hierarchy = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        return contours

    def _draw_contour(self, s: Settings, contours):
        self.video_output = self.frame.copy()
        for contour in contours:
            approx = cv.approxPolyDP(contour, s.contour_poly_threshold * cv.arcLength(contour, True), True)
            # 0.01 can be adjusted for recognition
            cv.drawContours(self.video_output, [approx], 0, (0, 0, 0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            if len(approx) == 3:
                cv.putText(self.video_output, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 4:
                x, y, w, h = cv.boundingRect(approx)
                aspect_ratio = float(w) / h
                if s.verbose:
                    print("Aspect ratio", aspect_ratio)
                if 0.95 <= aspect_ratio < 1.05:
                    cv.putText(self.video_output, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                else:
                    cv.putText(self.video_output, "Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 5:
                cv.putText(self.video_output, "Pentagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 10:
                cv.putText(self.video_output, "Star", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            else:
                cv.putText(self.video_output, "Circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    def _detect_lines(self, s: Settings):
        return cv.HoughLinesP(self.canny, 1, np.pi / 180, 60, np.array([]), 50, 5)

    def _draw_lines(self, s: Settings, lines):
        self.video_output = self.frame.copy()
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(self.video_output, (x1, y1), (x2, y2), (255, 0, 0), 3)

    def detect_objects(self, s: Settings):
        if s.edge_detection_type == 1:
            self._threshold(s)
            self._draw_contour(s, self._edge_contour(s, self.thrash))
        elif s.edge_detection_type == 2:
            self._edge_canny(s)
            self._draw_contour(s, self._edge_contour(s, self.canny))
        else:
            self._edge_canny(s)
            # self.draw_lines(s, self.detect_lines(s))

    def update_live_feed(self, s: Settings):
        self._video(s)

    def __del__(self) -> int:
        # TODO: Create deconstruct
        return 0
