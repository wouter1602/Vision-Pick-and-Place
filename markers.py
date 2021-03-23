#!/usr/bin/python3
from typing import Union, Tuple

import numpy as np
import cv2 as cv

from settings import Settings


class Markers:

    def __init__(self, s: Settings):
        self._aruco_dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)

        self.marker_frame = None
        self.warped_frame = None

    def _get_perspective(self, img: np.ndarray) -> Union[None, Tuple[np.ndarray, np.ndarray, np.ndarray]]:

        corners, ids, rejected = cv.aruco.detectMarkers(img, self._aruco_dictionary)

        if ids is None or len(ids) < 3:
            return None

        # TODO: Interpolate the last corner using 3 points

        marker_frame = cv.aruco.drawDetectedMarkers(img.copy(), corners, ids)

        img_corners = np.zeros([4, 2], dtype=np.float32)
        for i in range(len(ids)):
            img_corners[i][0] = (corners[i][0][0][0] + corners[i][0][2][0]) / 2
            img_corners[i][1] = (corners[i][0][0][1] + corners[i][0][2][1]) / 2

        return marker_frame, img_corners, ids

    def remove_warp(self, s: Settings, img: np.ndarray):
        # TODO: rotate frame using markers
        height, width = img.shape[:2]

        perspective_dst = np.float32([(width, 0),
                                      (0, 0),
                                      (width, height),
                                      (0, height)])

        self.marker_frame, img_corners, ids = self._get_perspective(img)

        matrix = cv.getPerspectiveTransform(img_corners, perspective_dst)

        self.warped_frame = cv.warpPerspective(img, matrix, (width, height), flags=cv.INTER_LINEAR)

        return self.marker_frame, self.warped_frame
