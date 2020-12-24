import PySimpleGUI as sg
import cv2 as cv
import numpy as np

from settings import Settings
from video import Video


class Ui:
    def __init__(self, s: Settings):
        if s.edge_detection_type == 1:
            self.layout = [
                [sg.Text('Vision Detection', size=(60, 1), justification='center')],
                [sg.Text('Original view', size=(60, 1), justification='left'),
                 sg.Text('Grayscale View', size=(60, 1), justification='right')],
                [sg.Image(filename='', size=(640, 480), key='-IMAGE NORMAL-', tooltip='Original view'),
                 sg.Image(filename='', size=(640, 480), key='-IMAGE GRAY-', tooltip='Grayscale view')],
                [sg.Text('Contour view', size=(60, 1), justification='left'),
                 sg.Text('Object view', size=(60, 1), justification='right')],
                [sg.Image(filename='', size=(640, 480), key='-IMAGE CONTOUR-', tooltip='Contour view'),
                 sg.Image(filename='', size=(640, 480), key='-IMAGE OBJECT-', tooltip='Object view')],
                [sg.Text('Canny thresholds')],
                [sg.Slider((0, 255), s.contour_threshold_A, 1, orientation='h', size=(40, 15), key='-CONTOUR SLIDER A-',
                           tooltip='Contour threshold A'),
                 sg.Slider((0, 255), s.contour_threshold_B, 1, orientation='h', size=(40, 15), key='-CONTOUR SLIDER B-',
                           tooltip='Contour threshold B')],
                [sg.Button('Exit', size=(10, 1))]
            ]
        elif s.edge_detection_type == 2:
            self.layout = [
                [sg.Text('Vision Detection', size=(60, 1), justification='center')],
                [sg.Text('Original view', size=(60, 1), justification='left'),
                 sg.Text('Grayscale View', size=(60, 1), justification='right')],
                [sg.Image(filename='', size=(640, 480), key='-IMAGE NORMAL-', tooltip='Original view'),
                 sg.Image(filename='', size=(640, 480), key='-IMAGE GRAY-', tooltip='Grayscale view')],
                [sg.Text('Contour view', size=(60, 1), justification='left'),
                 sg.Text('Object view', size=(60, 1), justification='right')],
                [sg.Image(filename='', size=(640, 480), key='-IMAGE CANNY-', tooltip='Canny view'),
                 sg.Image(filename='', size=(640, 480), key='-IMAGE OBJECT-', tooltip='Object view')],
                [sg.Text('Canny thresholds')],
                [sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), key='-CANNY SLIDER A-',
                           tooltip='Contour threshold A'),
                 sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), key='-CANNY SLIDER B-',
                           tooltip='Contour threshold B')],
                [sg.Slider((0.001, 0.1), s.contour_poly_threshold, 0.001, orientation='h', size=(40, 15),
                           key='-CANNY POLY SLIDER-', tooltip='Canny poly slider')],
                [sg.Button('Exit', size=(10, 1))]
            ]
        else:
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
                [sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), key='-CANNY SLIDER A-',
                           tooltip='Canny threshold A'),
                 sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), key='-CANNY SLIDER B-',
                           tooltip='Canny threshold B')],
                [sg.Button('Exit', size=(10, 1))]
            ]

        self._window = sg.Window('OpenCV TestWindow', self.layout, location=(800, 400))
        self._event = None
        self._values = None

    def update(self, s: Settings, v: Video) -> int:
        self._event, self._values = self._window.read(timeout=20)

        if self._event == sg.WIN_CLOSED or self._event == 'Exit':
            return 1

        if s.edge_detection_type == 1:
            s.contour_threshold_A = self._values['-CONTOUR SLIDER A-']
            s.contour_threshold_B = self._values['-CONTOUR SLIDER B-']
        elif s.edge_detection_type == 2:
            s.canny_threshold_A = self._values['-CANNY SLIDER A-']
            s.canny_threshold_B = self._values['-CANNY SLIDER B-']
        else:
            # Update Canny thresholds
            s.canny_threshold_A = self._values['-CANNY SLIDER A-']
            s.canny_threshold_B = self._values['-CANNY SLIDER B-']

        self._update_img(s, v)
        return 0

    def _update_img(self, s: Settings, v: Video):
        width = 640
        height = 480
        imgbytes_normal = cv.imencode('.png', v.frame)[1].tobytes()
        imgbytes_gray = cv.imencode('.png', v.grayscale)[1].tobytes()
        if s.edge_detection_type == 1:
            imgbytes_contour = cv.imencode('.png', v.thrash)[1].tobytes()
            imgbytes_object = cv.imencode('.png', v.video_output)[1].tobytes()
            self._window['-IMAGE CONTOUR-'].update(data=imgbytes_contour, size=(width, height))
            self._window['-IMAGE OBJECT-'].update(data=imgbytes_object, size=(width, height))
        elif s.edge_detection_type == 2:
            imgbytes_canny = cv.imencode('.png', v.canny)[1].tobytes()
            imgbytes_object = cv.imencode('.png', v.video_output)[1].tobytes()
            self._window['-IMAGE CANNY-'].update(data=imgbytes_canny, size=(width, height))
            self._window['-IMAGE OBJECT-'].update(data=imgbytes_object, size=(width, height))
        else:
            imgbytes_canny = cv.imencode('.png', v.canny)[1].tobytes()
            imgbytes_lines = cv.imencode('.png', v.video_output)[1].tobytes()
            self._window['-IMAGE CANNY-'].update(data=imgbytes_canny, size=(width, height))
            self._window['-IMAGE LINES-'].update(data=imgbytes_lines, size=(width, height))
        self._window['-IMAGE NORMAL-'].update(data=imgbytes_normal, size=(width, height))
        self._window['-IMAGE GRAY-'].update(data=imgbytes_gray, size=(width, height))

    def __del__(self) -> int:
        self._window.close()
        return 0
