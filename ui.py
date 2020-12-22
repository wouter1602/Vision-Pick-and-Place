import PySimpleGUI as sg
import cv2 as cv
import numpy as np

from settings import Settings
from video import Video


class Ui:
    def __init__(self):
        # self.layout = [[sg.Text('Some text')],
        #                [sg.Text('Some other text:'), sg.InputText()],
        #                [sg.Button('ok'), sg.Button('Cancel')]]

        self.layout = [
            [sg.Text('OpenCv Demo', size=(60, 1), justification='center')],
            [sg.Image(filename='', key='-IMAGE NORMAL-'),
             sg.Image(filename='', key="-IMAGE GRAY-")],
            [sg.Radio('None', 'Radio', True, size=(10, 1)),
             sg.Image(filename='', key="-IMAGE CANNY-")],
            [sg.Radio('Threshold', 'Radio', size=(10, 1), key='-THRESH-'),
             sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='-THRESH SLIDER-')],
            [sg.Radio('canny', 'Radio', size=(10, 1), key='-CANNY-'),
             sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER A-'),
             sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER B-')],
            [sg.Radio('blur', 'Radio', size=(10, 1), key='-BLUR-'),
             sg.Slider((1, 11), 1, 1, orientation='h', size=(40, 15), key='-BLUR SLIDER-')],
            [sg.Radio('hue', 'Radio', size=(10, 1), key='-HUE-'),
             sg.Slider((0, 255), 0, 1, orientation='h', size=(40, 15), key='-HUE SLIDER-')],
            [sg.Radio('enhance', 'Radio', size=(10, 1), key='-ENHANCE-'),
             sg.Slider((1, 255), 128, 1, orientation='h', size=(40, 15), key='-ENHANCE SLIDER-')],
            [sg.Button('Exit', size=(10, 1))]
        ]
        self.window = sg.Window('OpenCV TestWindow', self.layout, location=(800, 400))
        self.event = None
        self.values = None

    def update(self, s: Settings, v: Video) -> int:
        frame = v.frame.copy()
        self.event, self.values = self.window.read(timeout=20)

        if self.event == sg.WIN_CLOSED or self.event == 'Exit':
            return 1

        if self.values['-THRESH-']:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2LAB)[:, :, 0]
            frame = cv.threshold(frame, self.values['-THRESH SLIDER-'], 255, cv.THRESH_BINARY)[1]
        elif self.values['-CANNY-']:
            frame = cv.Canny(frame, self.values['-CANNY SLIDER A-'], self.values['-CANNY SLIDER B-'])
        elif self.values['-BLUR-']:
            frame = cv.GaussianBlur(frame, (21, 21), self.values['-BLUR SLIDER-'])
        elif self.values['-ENHANCE-']:
            enh_val = self.values['-ENHANCE SLIDER-'] / 40
            clahe = cv.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv.cvtColor(lab, cv.COLOR_Lab2BGR)
        self._update_img(v)
        return 0

    def _update_img(self, v: Video):
        imgbytes_normal = cv.imencode('.png', v.frame)[1].tobytes()
        imgbytes_gray = cv.imencode('.png', v.grayscale)[1].tobytes()
        imgbytes_canny = cv.imencode('.png', v.edge)[1].tobytes()
        self.window['-IMAGE NORMAL-'].update(data=imgbytes_normal)
        self.window['-IMAGE GRAY-'].update(data=imgbytes_gray)
        self.window['-IMAGE CANNY-'].update(data=imgbytes_canny)

    def __del__(self) -> int:
        self.window.close()
        return 0
