import PySimpleGUI as sg
import cv2 as cv
import numpy as np

from settings import Settings
from video import Video


class Ui:
    def __init__(self, s: Settings):
        self.layout = [

            [sg.Text('Vision Detection', size=(60, 1), justification='center')],
            [sg.Text('Original view', size=(60, 1), justification='left'),
             sg.Text('Grayscale View', size=(60, 1), justification='right')],
            [sg.Image(filename='', size=(640, 480), key='-IMAGE NORMAL-', tooltip='Original view'),
             sg.Image(filename='', size=(640, 480), key='-IMAGE GRAY-', tooltip='Grayscale view')],
            [sg.Text('Canny view', size=(60, 1), justification='left'),
             sg.Text('Lines view', size=(60, 1), justification='right')],
            [sg.Image(filename='', size=(640, 480), key='-IMAGE CANNY-', tooltip='Canny view'),
             sg.Image(filename='', size=(640, 480), key='-IMAGE LINES-', tooltip='Lines view')],
            [sg.Text('Canny thresholds')],
            [sg.Slider((0, 255), s.edge_threshold_A, 1, orientation='h', size=(40, 15), key='-CANNY SLIDER A-', tooltip='Canny threshold A'),
             sg.Slider((0, 255), s.edge_threshold_B, 1, orientation='h', size=(40, 15), key='-CANNY SLIDER B-', tooltip='Canny threshold B')],
            [sg.Button('Exit', size=(10, 1))]
        ]
        self._window = sg.Window('OpenCV TestWindow', self.layout, location=(800, 400))
        self._event = None
        self._values = None

    def update(self, s: Settings, v: Video) -> int:
        self._event, self._values = self._window.read(timeout=20)

        if self._event == sg.WIN_CLOSED or self._event == 'Exit':
            return 1

        # if self.values['-THRESH-']:
        #     frame = cv.cvtColor(frame, cv.COLOR_BGR2LAB)[:, :, 0]
        #     frame = cv.threshold(frame, self.values['-THRESH SLIDER-'], 255, cv.THRESH_BINARY)[1]
        # elif self.values['-CANNY-']:
        #     frame = cv.Canny(frame, self.values['-CANNY SLIDER A-'], self.values['-CANNY SLIDER B-'])
        # elif self.values['-BLUR-']:
        #     frame = cv.GaussianBlur(frame, (21, 21), self.values['-BLUR SLIDER-'])
        # elif self.values['-ENHANCE-']:
        #     enh_val = self.values['-ENHANCE SLIDER-'] / 40
        #     clahe = cv.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
        #     lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
        #     lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        #     frame = cv.cvtColor(lab, cv.COLOR_Lab2BGR)

        s.edge_threshold_A = self._values['-CANNY SLIDER A-']
        s.edge_threshold_B = self._values['-CANNY SLIDER B-']

        self._update_img(v)
        return 0

    def _update_img(self, v: Video):
        imgbytes_normal = cv.imencode('.png', v.frame)[1].tobytes()
        imgbytes_gray = cv.imencode('.png', v.grayscale)[1].tobytes()
        imgbytes_canny = cv.imencode('.png', v.edge)[1].tobytes()
        imgbytes_lines = cv.imencode('.png', v.video_lines)[1].tobytes()
        self._window['-IMAGE NORMAL-'].update(data=imgbytes_normal, size=(640, 480))
        self._window['-IMAGE GRAY-'].update(data=imgbytes_gray, size=(640, 480))
        self._window['-IMAGE CANNY-'].update(data=imgbytes_canny, size=(640, 480))
        self._window['-IMAGE LINES-'].update(data=imgbytes_lines, size=(640, 480))

    def __del__(self) -> int:
        self._window.close()
        return 0
