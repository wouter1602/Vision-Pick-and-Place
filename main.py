#!/usr/bin/python3

import numpy as np
import cv2 as cv
# import multiprocessing
# from dataclasses import dataclass
# import socket

from settings import Settings
from ui import Ui
from video import Video


def main() -> None:
    s = Settings()

    if s.display_output:
        win = Ui(s)
    else:
        win = None

    if s.verbose:
        print("Setup done, verbose is active")

    cap = Video(s)

    while True:
        # cap.detect_objects(s)
        cap.update_live_feed(s)
        # cv.imshow("Contour", cap.video_lines)

        if s.display_output:
            status_code = win.update(s, cap)
            if status_code == 2:
                cap.detect_objects(s)
            elif status_code != 0:
                break
            if win.update_detect:
                cap.detect_objects(s)
                win.update_detect = False
        # cv.waitKey(1)
    s.update_json()
    if s.display_output:
        del win
    del s
    del cap


if __name__ == '__main__':
    main()
