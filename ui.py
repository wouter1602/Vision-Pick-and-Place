import PySimpleGUI as sg
import cv2 as cv
import numpy as np
from typing import List

from settings import Settings
from video import Video


def layout_detection_type(s: Settings, width: int, height: int):
    if s.edge_detection_type == 1:
        detection_view = [
            [sg.Text('Contour View', size=(60, 1), justification='left', key='-VIEW 3 TEXT-'),
             sg.Text('Object View', size=(60, 1), justification='right', key='-VIEW 4 TEXT-')],
            [sg.Image(filename='', size=(width, height), key='-VIEW 3-', tooltip='Contour view'),
             sg.Image(filename='', size=(width, height), key='-VIEW 4-', tooltip='Object view')],
            [sg.Text('Canny thresholds')],
            [sg.Slider((0, 255), s.contour_threshold_A, 1, orientation='h', size=(40, 15), key='-SLIDER A-',
                       tooltip='Contour threshold A'),
             sg.Slider((0, 255), s.contour_threshold_B, 1, orientation='h', size=(40, 15), key='-SLIDER B-',
                       tooltip='Contour threshold B')],
            [sg.Slider((0.001, 0.1), s.contour_poly_threshold, 0.001, orientation='h', size=(40, 15),
                       key='-CANNY POLY SLIDER-', tooltip='Canny poly slider', visible=False)]
        ]
    elif s.edge_detection_type == 2:
        detection_view = [
            [sg.Text('Canny view', size=(60, 1), justification='left', key='-VIEW 3 TEXT-'),
             sg.Text('Object view', size=(60, 1), justification='right', key='-VIEW 4 TEXT-')],
            [sg.Image(filename='', size=(width, height), key='-VIEW 3-', tooltip='Canny view'),
             sg.Image(filename='', size=(width, height), key='-VIEW 4-', tooltip='Object view')],
            [sg.Text('Canny thresholds')],
            [sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), key='-SLIDER A-',
                       tooltip='Threshold threshold A'),
             sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), key='-SLIDER B-',
                       tooltip='Threshold threshold B')],
            [sg.Slider((0.001, 0.1), s.contour_poly_threshold, 0.001, orientation='h', size=(40, 15),
                       key='-CANNY POLY SLIDER-', tooltip='Canny poly slider', visible=True)]
        ]
    else:
        detection_view = [
            [sg.Text('Canny view', size=(60, 1), justification='left', key='-VIEW 3 TEXT-'),
             sg.Text('Lines view', size=(60, 1), justification='right', key='-VIEW 4 TEXT-')],
            [sg.Image(filename='', size=(width, height), key='-VIEW 3-', tooltip='Canny view'),
             sg.Image(filename='', size=(width, height), key='-VIEW 4-', tooltip='Object view')],
            [sg.Text('Canny thresholds')],
            [sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), key='-SLIDER A-',
                       tooltip='Canny threshold A'),
             sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), key='-SLIDER B-',
                       tooltip='Canny threshold B')],
            [sg.Slider((0.001, 0.1), s.contour_poly_threshold, 0.001, orientation='h', size=(40, 15),
                       key='-CANNY POLY SLIDER-', tooltip='Canny poly slider', visible=False)]
        ]
    return detection_view


class Ui:
    def __init__(self, s: Settings):
        # self.width = 640
        # self.height = 480
        # self.width = 320
        # self.height = 240
        self.width = 480
        self.height = 360

        sg.theme('Topanga')
        if s.edge_detection_type == 1:
            standard_type = 'Threshold Detection'
        elif s.edge_detection_type == 2:
            standard_type = 'Canny + Threshold'
        else:
            standard_type = 'Canny Detection'
        begin_layout = [
            [sg.Combo(['Canny Detection', 'Threshold Detection', 'Canny + Threshold'], standard_type,
                      key='-DETECTION TYPE-'),
             sg.Text('Vision Detection', size=(60, 1), justification='center')],
            [sg.Text('Original view', size=(60, 1), justification='left'),
             sg.Text('Grayscale View', size=(60, 1), justification='right')],
            [sg.Image(filename='', size=(self.width, self.height), key='-IMAGE NORMAL-', tooltip='Original view'),
             sg.Image(filename='', size=(self.width, self.height), key='-IMAGE GRAY-', tooltip='Grayscale view')],
        ]
        detection_view = layout_detection_type(s, self.width, self.height)

        button_view = [
            [sg.Radio('Auto detect', "Radio", default=s.autodetect, key='-RADIO AUTO-'),
             sg.Radio('Manual detect', "Radio", default=(not s.autodetect), key='-RADIO MANUAL-')],
            [sg.Button('Exit', size=(10, 1)),
             sg.Button('Detect', size=(10, 1), disabled=s.autodetect, key='-DETECT BUTTON-')]
        ]

        self.layout = begin_layout + detection_view + button_view
        self.update_detect = False
        self._window = sg.Window('OpenCV TestWindow', self.layout, location=(800, 400), icon='./Image/Eye.png')

        self._event = None
        self._values = None

    def update(self, s: Settings, v: Video) -> int:
        self._event, self._values = self._window.read(timeout=20)

        if self._event == sg.WIN_CLOSED or self._event == 'Exit':
            return 1
        elif self._event == '-DETECT BUTTON-':
            self.update_detect = True

        if self._update_layout(s):
            return 2

        if self._values['-RADIO AUTO-'] and s.autodetect != 1:
            s.autodetect = 1
            self._window['-DETECT BUTTON-'].update(disabled=True)
        elif self._values['-RADIO MANUAL-'] and s.autodetect != 0:
            s.autodetect = 0
            self._window['-DETECT BUTTON-'].update(disabled=False)

        if s.edge_detection_type == 1:
            s.contour_threshold_A = self._values['-SLIDER A-']
            s.contour_threshold_B = self._values['-SLIDER B-']
        elif s.edge_detection_type == 2:
            s.canny_threshold_A = self._values['-SLIDER A-']
            s.canny_threshold_B = self._values['-SLIDER B-']
        else:
            # Update Canny thresholds
            s.canny_threshold_A = self._values['-SLIDER A-']
            s.canny_threshold_B = self._values['-SLIDER B-']

        self._update_img(s, v)
        return 0

    def _update_layout(self, s) -> bool:
        if self._values['-DETECTION TYPE-'] == 'Threshold Detection' and s.edge_detection_type != 1:
            s.edge_detection_type = 1
            self._window['-VIEW 3 TEXT-'].update(value='Contour View')
            self._window['-VIEW 4 TEXT-'].update(value='Object View')
            self._window['-SLIDER A-'].update(range=(0, 255), value=s.contour_threshold_A)
            self._window['-SLIDER B-'].update(range=(0, 255), value=s.contour_threshold_B)
            self._window['-CANNY POLY SLIDER-'].update(visible=False)
            return True
        elif self._values['-DETECTION TYPE-'] == 'Canny + Threshold' and s.edge_detection_type != 2:
            s.edge_detection_type = 2
            self._window['-VIEW 3 TEXT-'].update(value='Canny View')
            self._window['-VIEW 4 TEXT-'].update(value='Object View')
            self._window['-SLIDER A-'].update(range=(0, 255), value=s.canny_threshold_A)
            self._window['-SLIDER B-'].update(range=(0, 255), value=s.canny_threshold_B)
            self._window['-CANNY POLY SLIDER-'].update(range=(0.001, 0.1), visible=True, value=s.contour_poly_threshold)
            return True
        elif self._values['-DETECTION TYPE-'] == 'Canny Detection' and s.edge_detection_type != 0:
            s.edge_detection_type = 0
            self._window['-VIEW 3 TEXT-'].update(value='Canny View')
            self._window['-VIEW 4 TEXT-'].update(value='Lines View')
            self._window['-SLIDER A-'].update(range=(0, 255), value=s.canny_threshold_A)
            self._window['-SLIDER B-'].update(range=(0, 255), value=s.canny_threshold_A)
            self._window['-CANNY POLY SLIDER-'].update(visible=False)
            return True
        else:
            return False

    def _update_img(self, s: Settings, v: Video):
        if s.edge_detection_type == 1:
            view_3_view = cv.resize(v.thrash, (self.width, self.height))
        elif s.edge_detection_type == 2:
            view_3_view = cv.resize(v.canny, (self.width, self.height))
        else:
            view_3_view = cv.resize(v.canny, (self.width, self.height))
        normal_view = cv.resize(v.frame, (self.width, self.height))
        output_view = cv.resize(v.video_output, (self.width, self.height))
        gray_view = cv.resize(v.grayscale, (self.width, self.height))
        imgbytes_view_3 = cv.imencode('.png', view_3_view)[1].tobytes()
        imgbytes_view_4 = cv.imencode('.png', output_view)[1].tobytes()
        imgbytes_normal = cv.imencode('.png', normal_view)[1].tobytes()
        imgbytes_gray = cv.imencode('.png', gray_view)[1].tobytes()
        self._window['-IMAGE NORMAL-'].update(data=imgbytes_normal, size=(self.width, self.height))
        self._window['-IMAGE GRAY-'].update(data=imgbytes_gray, size=(self.width, self.height))
        self._window['-VIEW 3-'].update(data=imgbytes_view_3, size=(self.width, self.height))
        self._window['-VIEW 4-'].update(data=imgbytes_view_4, size=(self.width, self.height))

    def __del__(self) -> int:
        self._window.close()
        return 0
