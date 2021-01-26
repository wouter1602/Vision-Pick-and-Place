# Video Class with all the object recognition functions

from settings import Settings

from typing import List, Union
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
    blob: np.ndarray

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
            self._cap.set(cv.CAP_PROP_FRAME_WIDTH, s.frame_width)
            self._cap.set(cv.CAP_PROP_FRAME_HEIGHT, s.frame_height)
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
        self.blank = self.frame.copy()
        self.blob = self.frame.copy()

    @staticmethod
    def _get_video(s: Settings, cap: Union[np.ndarray, cv.VideoCapture]) -> np.ndarray:
        """
        Updates the most recent video frame if the program is using a webcam. Otherwise will return the data in cap
        :param s: Settings object used to store threshold and camera used data
        :type s: Settings
        :param cap: Object for VideoCapture or np array frame of loaded image
        :type cap: Union[np.ndarray, cv.VideoCapture]
        :return: frame image
        :rtype: np.ndarray
        """
        if not s.use_test_image:  # Function doesn't need to update the video frame if it's a static image
            _, frame = cap.read()
            return frame
        else:
            return cap

    @staticmethod
    def _convert_to_grayscale(frame: np.ndarray) -> np.ndarray:
        """
        Converts the image to a grayscale
        :param frame: cv BGR image frame that gets converted to grayscale
        :type frame: np.ndarray
        :return: grayscale image
        :rtype: np.ndarray
        """
        grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return grayscale

    @staticmethod
    def _edge_canny(s: Settings, frame: np.ndarray) -> np.ndarray:
        """
        Uses the "canny_threshold_A" and "canny_threshold_B" to create an Canny view of the objects.
        This function first grabs the most recent camera image an converts it to grayscale.
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :param frame: grayscale image frame for canny edge detection
        :type frame: np.ndarray
        :return: canny image
        :rtype: np.ndarray
        """
        canny = cv.Canny(frame, s.canny_threshold_A, s.canny_threshold_B)
        return canny

    @staticmethod
    def _edge_contour(frame: np.ndarray) -> List:
        """
        Detects contours found in the image
        :param frame: grayscale image frame for contour edge detection
        :type frame: np.ndarray
        :return: List with all the found contours
        """
        # hierarchy is not used
        contours, hierarchy = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def _edge_blob(frame: np.ndarray) -> np.ndarray:
        """
        TODO: not yet implemented
        :param frame:
        :type frame: np.ndarray
        :return:
        :rtype: np.ndarray
        """
        detector = cv.SimpleBlobDetector()
        keypoints = detector.detect(frame)
        return keypoints

    @staticmethod
    def _edge_threshold(s: Settings, frame: np.ndarray, threshold_A=None, threshold_B=None) -> np.ndarray:
        """
        Uses the "contour_threshold_A" and "contour_threshold_B" to create an threshold view of the objects.
        Turns part of the image white of black based on those thresholds.
        This function first grabs the most recent camera image an converts it to grayscale.
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :param frame: grayscale image for threshold detection
        :type frame: np.ndarray
        :param threshold_A:
        :type threshold_A: Union[int, None]
        :param threshold_B:
        :type threshold_B: Union[int, None]
        :return: threshold image
        :rtype: np.ndarray
        """
        if threshold_A is None:
            threshold_A = s.contour_threshold_A
        if threshold_B is None:
            threshold_B = s.contour_threshold_B

        ret, thresh = cv.threshold(frame, threshold_A, threshold_B, cv.THRESH_BINARY)
        return thresh

    @staticmethod
    def _draw_every_contour(s: Settings, contours: Union[np.ndarray, List], width: int, height: int) -> np.ndarray:
        """
        Draws every contour on an empty canvas created using _edge_contour function
        :param s: Settigns object used to store threshold and camera used data
        :type s: Settings
        :param contours: List or np array filled with contour data
        :type contours: Union[np.ndarray, List]
        :param width: frame width
        :type width: int
        :param height: frame height
        :type height: int
        :return: Black and white image with with the contour lines drawn on
        :rtype: np.ndarray
        """
        frame = np.zeros(shape=(width, height), dtype=np.uint8)
        for contour in contours:
            approx = cv.approxPolyDP(contour, s.contour_poly_threshold * cv.arcLength(contour, True), True)
            cv.drawContours(frame, [approx], 0, (255, 255, 255), 1)
        return frame

    @staticmethod
    def _draw_contour(s: Settings, frame: np.ndarray, contours: List) -> np.ndarray:
        """
        Function draws the found lines on the current view window.
        Uses the "contour_poly_threshold" to approximate the shapes of the objects.
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :param frame: image used to draw detected contours over
        :type frame: np.ndarray
        :param contours: List with all the contours in the found image
        :type contours: List
        :return: Image with contour lines drawn on
        :rtype: np.ndarray
        """
        video_output = frame.copy()
        for contour in contours:
            approx = cv.approxPolyDP(contour, s.contour_poly_threshold * cv.arcLength(contour, True), True)
            # contour_poly_threshold can be adjusted for recognition
            # approximates the contours found into shapes
            # cv.drawContours(self.video_output, [approx], 0, (0, 255, 0), 2)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            # if approx has 3 elements the object is a triangle
            # TODO: get centre of a poligon
            x_low = np.amin(approx[:, 0, 0])
            x_high = np.amax(approx[:, 0, 0])
            y_low = np.amin(approx[:, 0, 1])
            y_high = np.amax(approx[:, 0, 1])

            x_center = x_high - x_low
            y_center = y_high - y_low
            if Video._check_pixel(video_output, s.triangle_1, x_center, y_center, 5):
                print("Good")
            if len(approx) == 3:
                cv.putText(video_output, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                cv.drawContours(video_output, [approx], 0, (0, 0, 255), 2)
                if s.verbose:
                    print("Found triangle at:", x, ", ", y)
            # if approx has 4 element the object is a square or rectangle
            elif len(approx) == 4:
                x, y, w, h = cv.boundingRect(approx)
                cv.drawContours(video_output, [approx], 0, (0, 0, 255), 2)
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio < 1.05:
                    cv.putText(video_output, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    if s.verbose:
                        print("Found square at:", x, ", ", y)
                else:
                    cv.putText(video_output, "Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    if s.verbose:
                        print("Found rectangle at:", x, ", ", y)
            else:
                str = "No idea it has {} lines".format(len(approx))
                cv.putText(video_output, str, (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                cv.drawContours(video_output, [approx], 0, (0, 255, 255), 2)
        return video_output

    @staticmethod
    def _check_pixel(frame: np.ndarray, colour: int, x: int, y: int, sigma: Union[float, int]) -> bool:
        R = (colour >> 0) & 0xFF
        G = (colour >> 8) & 0xFF
        B = (colour >> 16) & 0xFF

        if (B - sigma) < frame[x, y, 0] < (B + sigma) and (G - sigma) < frame[x, y, 1] < (G + sigma) and (R - sigma) < \
                frame[x, y, 2] < (R + sigma):
            return True
        else:
            return False

    @staticmethod
    def _detect_lines(frame: np.ndarray) -> np.array:
        """
        Uses the HoughLineP function to detect lines.
        :param frame: grayscale image for line detection
        :type frame: np.ndarray
        :return: Houghlinesp array with lines
        :rtype: np.ndarray
        """
        return cv.HoughLinesP(image=frame, rho=1, theta=np.pi / 180, threshold=50, lines=np.array([]), minLineLength=10,
                              maxLineGap=5)

    @staticmethod
    def _draw_lines(lines: np.array, width: int, height: int) -> np.ndarray:
        """
        Draws the lines found using the _detect_lines() function.
        :param lines: List with lines found in the image
        :type lines: np.array
        :param width: frame width
        :type width: int
        :param height: frame height
        :type height: int
        :return: black and white frame with the detected lines
        :rtype: np.ndarray
        """
        video_output = np.zeros((width, height), dtype=np.uint8)
        for x1, y1, x2, y2 in lines:
            cv.line(video_output, (x1, y1), (x2, y2), (255, 0, 0), 1)
        return video_output

    @staticmethod
    def _dilate_edges(frame: np.ndarray, kernel=None, iterations=1) -> np.ndarray:
        """
        Enlarges the edges found using the _edge_canny() function. This is done to remove as many double lines as
        possible
        :param frame: grayscale image used to dilate
        :type frame: np.ndarray
        :param kernel: kernel size used to dilate edges, if kernel is none size will be 3 x 3
        :type kernel: Union[np.ndarray, None]
        :param iterations: Non negative int for how many iterations the dilate function should be used for
        :type iterations: int
        :return: Dilated image
        :rtype: np.ndarray
        """
        if kernel is None:
            kernel = np.ones((3, 3), np.uint8)

        dilate = cv.dilate(frame, kernel, iterations=iterations)
        return dilate

    @staticmethod
    def _erode_edges(frame: np.ndarray, kernel=None, iterations=1) -> np.ndarray:
        """
        Erodes the edges of the detected lines.
        This wil make the lines thinner and easier to detect using the detect lines functions.
        :param frame: grayscale image used to erode
        :type frame: np.ndarray
        :param kernel: kernel size used to erode edges, if kernel is none size will be 3 x 3
        :type kernel: Union[np.ndarray, None]
        :return: Eroded image
        :rtype: np.ndarray
        """
        if kernel is None:
            kernel = np.ones((3, 3), np.uint8)

        erode = cv.erode(frame, kernel, iterations=iterations)
        return erode

    @staticmethod
    def _blur_edges(s: Settings, frame: np.ndarray, ksize=None) -> np.ndarray:
        """
        Blurs image using the ksize
        :param s: Settigns object used to store thresholds and camera used data
        :type s: Settings
        :param frame: grayscale image used to blur
        :type frame: np.ndarray
        :param ksize: Tuple with the blur parameters if ksize=None the values are used from the Settings object
        :type ksize: Union[Tuple, None]
        :return: Blurred image
        :rtype: np.ndarray
        """
        if ksize is None:
            ksize = (int(s.blur_threshold_A), int(s.blur_threshold_B))

        blur = cv.blur(frame, ksize=ksize)
        return blur

    def detect_objects(self, s: Settings) -> None:
        """
        Uses the in Settings specified method to detect the object
        :param s: Settings object used to store thresholds and camera used data
        :type s: Settings
        :return: None
        """
        self.frame = self._get_video(s, self._cap)
        self.grayscale = self._convert_to_grayscale(self.frame)
        width, height = self.frame.shape[0:2]

        if s.edge_detection_type == 1:  # Only threshold detection
            self.thrash = self._edge_threshold(s, self.grayscale)
            self.video_output = self._draw_contour(s, self.frame, self._edge_contour(self.thrash))
        elif s.edge_detection_type == 2:  # Threshold + Canny shape detection
            gausian_blur = cv.GaussianBlur(self.grayscale, (5, 5), sigmaX=0)
            self.thrash = self._edge_threshold(s, gausian_blur)
            self.canny = self._edge_canny(s, self.thrash)
            self.dilate = self._dilate_edges(self.canny, iterations=s.dilate_iterations)
            self.erode = self._erode_edges(self.dilate, iterations=s.erode_iterations)
            self.blur = self._blur_edges(s, self.erode)
            contours = self._edge_contour(self.blur)
            self.video_output = self._draw_contour(s, self.frame, contours)
            cv.imwrite('./output.bmp', self.video_output)
        elif s.edge_detection_type == 3:  # Blob + Canny shape detection
            self.blob = self._edge_blob(self.grayscale)
            self.canny = self._edge_canny(s, self.blob)
        else:  # Simple Canny method
            self._edge_canny(s, self.grayscale)

    def update_live_feed(self, s: Settings) -> None:
        """
        Public method to update the video feed
        :param s: Settings object used to store threshold and camera used data
        :type s: Settings
        :return: None
        """
        self.frame = self._get_video(s, self._cap)

    def __del__(self) -> int:
        # TODO: Create deconstruct
        return 0
