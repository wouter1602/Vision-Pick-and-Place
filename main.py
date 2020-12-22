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
        cap.detect_objects(s)

        cv.imshow("Contour", cap.video_lines)

        if s.display_output:
            if win.update(s, cap) != 0:
                break
        cv.waitKey(1)
    s.update_json()
    if s.display_output:
        del win
    del s
    del cap


if __name__ == '__main__':
    main()
