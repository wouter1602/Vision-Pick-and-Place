# Video Class with all the object recognition functions

from settings import Settings

from typing import List
import cv2 as cv
import numpy as np


class Video:
    # Type hinting for all the public variables
    frame: np.ndarray
    grayscale: np.ndarray
    blur: np.ndarray
    canny: np.ndarray
    thrash: np.ndarray
    video_output: np.ndarray
    dilate: np.ndarray
    erode: np.ndarray
    morphologyEx: np.ndarray

    # Type hinting for all private variables
    _cap: cv.VideoCapture

    def __init__(self, s: Settings):
        """
        Opens camera in the in Settings object classified location
        :param s: Settings object used to store thresholds and camera used data
        """
        if s.use_test_image:
            # If defined in the Settings object the program wil use a static test image for testing purposes
            self._cap = cv.imread(s.test_image)
            self.frame = cv.imread(s.test_image)
        else:
            self._cap = cv.VideoCapture(s.capture_device)
            _, self.frame = self._cap.read()

        # This defines all the transformations that you can get of the images
        self.grayscale = self.frame.copy()
        self.blur = self.frame.copy()
        self.canny = self.frame.copy()
        self.thrash = self.frame.copy()
        self.video_output = self.frame.copy()
        self.dilate = self.frame.copy()
        self.erode = self.frame.copy()
        self.morphologyEx = self.frame.copy()

    def _get_video(self, s: Settings) -> None:
        """
        Gets the most recent image of the camera or returns static image if defined in the Settings object.
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :return: None
        """
        if not s.use_test_image:  # Function doesn't need to update the video frame if it's a static image
            _, self.frame = self._cap.read()

    def _convert_to_grayscale(self) -> None:
        """
        Converts the image to a grayscale
        :return: None
        """
        self.grayscale = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

    def _edge_canny(self, s: Settings) -> None:
        """
        Uses the "canny_threshold_A" and "canny_threshold_B" to create an Canny view of the objects.
        This function first grabs the most recent camera image an converts it to grayscale.
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :return: None
        """
        self._get_video(s)
        self._convert_to_grayscale()

        self.canny = cv.Canny(self.grayscale, s.canny_threshold_A, s.canny_threshold_B)

    def _edge_contour(self, frame: np.ndarray) -> List:
        """
        Detects contours found in the image
        :param frame: current frame you want edge detection on
        :type frame: np.ndarray
        :return: List with all the found contours
        """
        # hierarchy is not used
        contours, hierarchy = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        return contours

    def _threshold(self, s: Settings) -> None:
        """
        Uses the "contour_threshold_A" and "contour_threshold_B" to create an threshold view of the objects.
        Turns part of the image white of black based on those thresholds.
        This function first grabs the most recent camera image an converts it to grayscale.
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :return: None
        """
        self._get_video(s)
        self._convert_to_grayscale()

        ret, self.thrash = cv.threshold(self.grayscale, s.contour_threshold_A, s.contour_threshold_B,
                                        cv.CHAIN_APPROX_NONE)

    def _draw_contour(self, s: Settings, contours: List) -> None:
        """
        Function draws the found lines on the current view window.
        Uses the "contour_poly_threshold" to approximate the shapes of the objects.
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :param contours: List with all the contours in the found image
        :type contours: List
        :return: None
        """
        self.video_output = self.frame.copy()
        for contour in contours:
            approx = cv.approxPolyDP(contour, s.contour_poly_threshold * cv.arcLength(contour, True), True)
            # contour_poly_threshold can be adjusted for recognition
            # approximates the contours found into shapes
            cv.drawContours(self.video_output, [approx], 0, (0, 0, 0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            # if approx has 3 elements the object is a triangle
            if len(approx) == 3:
                cv.putText(self.video_output, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                if s.verbose:
                    print("Found triangle at:", x, ", ", y)
            # if approx has 4 element the object is a square or rectangle
            elif len(approx) == 4:
                x, y, w, h = cv.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio < 1.05:
                    cv.putText(self.video_output, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    if s.verbose:
                        print("Found square at:", x, ", ", y)
                else:
                    cv.putText(self.video_output, "Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    if s.verbose:
                        print("Found rectangle at:", x, ", ", y)

    def _detect_lines(self) -> np.array:
        """
        Uses the HoughLineP function to detect lines.
        :return:
        """
        return cv.HoughLinesP(self.canny, 1, np.pi / 180, 60, np.array([]), 50, 5)

    def _draw_lines(self, lines: np.array) -> None:
        """
        Draws the lines found using the _detect_lines() function.
        :param lines: List with lines found in the image
        :type lines: np.array
        :return: None
        """
        self.video_output = self.frame.copy()
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(self.video_output, (x1, y1), (x2, y2), (255, 0, 0), 3)

    def _dilate_edges(self, iterations=1, frame=None) -> None:
        """
        Enlarges the edges found using the _edge_canny() function. This is done to remove as many double lines as
        possible
        :param iterations: Non negative int for how many iterations the dilate function should be used for
        :type iterations: int
        :return: None
        """
        kernel = np.ones((5, 5), np.uint8)
        if frame is not None:  # if no input is given uses the canny data
            self.dilate = cv.dilate(frame, kernel, iterations=iterations)
        else:
            self.dilate = cv.dilate(self.canny, kernel, iterations=iterations)

    def _erode_edges(self, iterations=1, frame=None) -> None:
        """
        Erodes the edges of the detected lines.
        This wil make the lines thinner and easier to detect using the detect lines functions.
        :return: None
        """
        kernel = np.ones((5, 5), np.uint8)
        self.erode = cv.erode(self.dilate, kernel, iterations=iterations)
        self.morphologyEx = cv.morphologyEx(self.erode, cv.MORPH_GRADIENT, kernel)

    def detect_objects(self, s: Settings) -> None:
        """
        Uses the in Settings specified method to detect the object
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :return: None
        """
        if s.edge_detection_type == 1:  # Threshold method
            self._threshold(s)
            self._draw_contour(s, self._edge_contour(self.thrash))
        elif s.edge_detection_type == 2:  # Canny + filter method
            self._edge_canny(s)
            self._dilate_edges(1)
            self._erode_edges()
            self._draw_contour(s, self._edge_contour(self.erode))
        elif s.edge_detection_type == 3:  # Blob + Canny filter method
            # detect blob
            # maybe dilate and erode necessary
            # detect edges - canny
            print("lmao")
        else:  # Simple Canny method
            self._edge_canny(s)
            # self.draw_lines(s, self.detect_lines(s))

    def update_live_feed(self, s: Settings) -> None:
        """
        Public method to update the video feed
        :param s: Settings object used to store threshold and camera used data
        :type s: Settings
        :return: None
        """
        self._get_video(s)

    def __del__(self) -> int:
        # TODO: Create deconstruct
        return 0
