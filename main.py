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
        win = Ui()
    else:
        win = None

    if s.verbose:
        print("Setup done, verbose is active")

    cap = Video(s)

    while True:

        cap.edge_detection(s)
        cap.detect_lines(s)
        cap.draw_lines(s)

        # if s.verbose:
        # cv.imshow("Frame", cap.frame)
        # cv.imshow("Grayscale", cap.grayscale)
        # cv.imshow("Blur", cap.blur)
        # cv.imshow("Edges", cap.edge)
        # cv.imshow("Frame /W Lines", cap.video_lines)

        # key = cv.waitKey(1)
        # if key == 27:  # Key 'S'
        #      break
        if s.display_output:
            if win.update(s, cap) != 0:
                break
        cv.waitKey(1)


    # cv.waitKey(0)

    cv.destroyAllWindows()
    if s.display_output:
        del win
    del s
    del cap


if __name__ == '__main__':
    main()
