import PySimpleGUI as sg
import cv2 as cv
import numpy as np
from typing import List, Union

from settings import Settings
from video import Video


def main_layout(s: Settings) -> List:
    """
    Creates an list with the layout of the main window, costum to the edge detection type
    :param s: settings object used for edge_detection_type
    :return: List with the layout
    :rtype: List
    """
    if s.edge_detection_type == 1:
        standard_type = 'Threshold Detection'
    elif s.edge_detection_type == 2:
        standard_type = 'Canny + Threshold'
    elif s.edge_detection_type == 3:
        standard_type = 'Blob + Canny'
    else:
        standard_type = 'Canny Detection'
    layout = [
        [sg.Combo(['Canny Detection', 'Threshold Detection', 'Canny + Threshold', 'Blob + Canny'], standard_type,
                  key='-DETECTION TYPE-'),
         sg.Text('Vision Detection', size=(60, 1), justification='center')],
        [sg.Text('Original view', size=(60, 1), justification='left'),
         sg.Text('output view', size=(60, 1), justification='right')],
        [sg.Image(filename='', size=(s.image_width, s.image_height), key='-IMAGE NORMAL-',
                  tooltip='Original view'),
         sg.Image(filename='', size=(s.image_width, s.image_height), key='-IMAGE OUTPUT-',
                  tooltip='Output view')],
        [sg.Radio('auto detect', "detection radio", default=s.autodetect, key='-RADIO AUTO-'),
         sg.Radio('Manual detect', "detection radio", default=(not s.autodetect), key='-RADIO MANUAL-')],
        [sg.Button('Exit', size=(10, 1)),
         sg.Button('Detect', size=(10, 1), disabled=s.autodetect, key='-DETECT BUTTON-'),
         sg.Button('Detect variables', size=(10, 1), key='-MORE BUTTON-')]
    ]
    return layout


def detect_layout(s: Settings) -> List:
    """
    Creates an list with the layout of the dection window, costum to the edge detection type
    :param s: settings object used for edge_detection_type
    :return: List with the layout
    :rtype: List
    """
    layout = [
        [sg.Text('Detection type', size=(60, 1), justification='center', key='-DETECTION TYPE TEXT-')],
        [sg.Text('Window 1', size=(60, 1), justification='left', key='-WINDOW 1 TEXT-'),
         sg.Text('Window 2', size=(60, 1), justification='right', key='-WINDOW 2 TEXT-')],
        [sg.Image(filename='', size=(s.image_width, s.image_height), key='-WINDOW 1-'),
         sg.Image(filename='', size=(s.image_width, s.image_height), key='-WINDOW 2-')],
        [sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), tooltip='Slider A',
                   key='-SLIDER WINDOW 1 A-'),
         sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), tooltip='Slider A',
                   key='-SLIDER WINDOW 2 A-')],
        [sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), tooltip='Slider B',
                   key='-SLIDER WINDOW 1 B-'),
         sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), tooltip='Slider B',
                   key='-SLIDER WINDOW 2 B-')],
        [sg.Text('Window 3', size=(60, 1), justification='left', key='-WINDOW 3 TEXT-'),
         sg.Text('Window 4', size=(60, 1), justification='right', key='-WINDOW 4 TEXT-')],
        [sg.Image(filename='', size=(s.image_width, s.image_height), key='-WINDOW 3-'),
         sg.Image(filename='', size=(s.image_width, s.image_height), key='-WINDOW 4-')],
        [sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), tooltip='Slider A',
                   key='-SLIDER WINDOW 3 A-'),
         sg.Slider((0, 255), s.canny_threshold_A, 1, orientation='h', size=(40, 15), tooltip='Slider A',
                   key='-SLIDER WINDOW 4 A-')],
        [sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), tooltip='Slider B',
                   key='-SLIDER WINDOW 3 B-'),
         sg.Slider((0, 255), s.canny_threshold_B, 1, orientation='h', size=(40, 15), tooltip='Slider B',
                   key='-SLIDER WINDOW 4 B-')],
        [sg.Radio('Erode view', 'view', default=True, visible=False, key='-RADIO ERODE-'),
         sg.Radio('Dilate view', 'view', default=False, visible=False, key='-RADIO DILATE-'),
         sg.Radio('Canny view', 'view 1', default=True, visible=False, key='-RADIO CANNY-'),
         sg.Radio('Threshold view', 'view 1', default=False, visible=False, key='-RADIO THRESHOLD-')],
        [sg.Button('Exit', size=(10, 1)),
         sg.Button('Detect', size=(10, 1), disabled=s.autodetect, key='-DETECT BUTTON-')]
    ]
    return layout


class Ui:
    def __init__(self, s: Settings):
        """
        Creates the main window
        :param s: Settings object used for edge detection type
        """
        sg.theme('Topanga')

        self.layout = main_layout(s)
        self.extra_layout = detect_layout(s)
        self.update_detect = False
        self._window = sg.Window('Vision A3 detection debugger', self.layout, location=(800, 400),
                                 icon='./Image/Eye.png')
        self._extra_window = None
        self._event = None
        self._values = None
        self._event_extra = None
        self._values_extra = None
        self._extra_window_bool = False

    def update(self, s: Settings, v: Video) -> int:
        """
        Updates the images in the frames and the values in the edge detection variables
        :param s: Settings object for the edge detection variables
        :type s: Settings
        :param v: Video object with all the frames that needs to be drawn
        :type v: Video
        :return: 0 if the main program doesn't need to do anything
        :return: 1 if the "exit" button or the close button is pressed
        :return: 2 if the extra window needs to be rendered
        :return: 3 if the ëxit"button or the close button of the extra window is pressed
        :rtype: int
        """
        self._event, self._values = self._window.read(timeout=20)
        if self._extra_window_bool:
            self._event_extra, self._values_extra = self._extra_window.read(timeout=20)

        if self._extra_window_bool:
            if self._event_extra == sg.WIN_CLOSED or self._event_extra == 'Exit':
                return 3
            elif self._event_extra == '-DETECT BUTTON-':
                self.update_detect = True

        if self._event == sg.WIN_CLOSED or self._event == 'Exit':
            return 1
        elif self._event == '-DETECT BUTTON-':
            self.update_detect = True
        elif self._event == '-MORE BUTTON-' and not self._extra_window_bool:
            self._extra_window_bool = True
            self.extra_layout = detect_layout(s)
            self._extra_window = sg.Window('Detect View', self.extra_layout, location=(800, 400),
                                           icon='./Image/Eye.png', finalize=True)
            s.edge_detection_type = -1
            self._update_extra_layout(s)
            self._event_extra, self._values_extra = self._extra_window.read(timeout=20)

        if self._extra_window_bool:
            if self._update_extra_layout(s):
                return 2
            self._update_extra_window(s)

        if self._update_layout(s):
            return 2

        if self._values['-RADIO AUTO-'] and s.autodetect != 1:
            s.autodetect = 1
            self._window['-DETECT BUTTON-'].update(disabled=True)
            if self._extra_window_bool:
                self._extra_window['-DETECT BUTTON-'].update(disabled=True)
        elif self._values['-RADIO MANUAL-'] and s.autodetect != 0:
            s.autodetect = 0
            self._window['-DETECT BUTTON-'].update(disabled=False)
            if self._extra_window_bool:
                self._extra_window['-DETECT BUTTON-'].update(disabled=False)

        self._update_img(s, v)
        if self._extra_window_bool:
            self._update_extra_img(s, v)
        return 0

    def _update_layout(self, s) -> bool:
        """
        simple check if the layout needs to be updated
        :param s: Settings used for edge_detection_type
        :return: True if it needs to be updated
        :return: False if it is not needed
        :rtype: bool
        """
        if self._values['-DETECTION TYPE-'] == 'Threshold Detection' and s.edge_detection_type != 1:
            s.edge_detection_type = 1
            return True
        elif self._values['-DETECTION TYPE-'] == 'Canny + Threshold' and s.edge_detection_type != 2:
            s.edge_detection_type = 2
            return True
        elif self._values['-DETECTION TYPE-'] == 'Blob + Canny' and s.edge_detection_type != 3:
            s.edge_detection_type = 3
            return True
        elif self._values['-DETECTION TYPE-'] == 'Canny Detection' and s.edge_detection_type != 0:
            s.edge_detection_type = 0
            return True
        else:
            return False

    def _update_extra_window(self, s) -> None:
        """
        Saves the values changed using the sliders in de Settings object
        :param s: Settings object used to store detection values
        :type s: Settings
        :return: None
        :rtype: None
        """
        # TODO: create update fields
        if s.edge_detection_type == 1:
            s.contour_threshold_A = self._values_extra['-SLIDER WINDOW 2 A-']
            s.contour_threshold_B = self._values_extra['-SLIDER WINDOW 2 B-']
        elif s.edge_detection_type == 2:
            s.contour_threshold_A = self._values_extra['-SLIDER WINDOW 1 A-']
            s.contour_threshold_B = self._values_extra['-SLIDER WINDOW 1 B-']
            s.canny_threshold_A = self._values_extra['-SLIDER WINDOW 2 A-']
            s.canny_threshold_B = self._values_extra['-SLIDER WINDOW 2 B-']
            s.dilate_iterations = int(self._values_extra['-SLIDER WINDOW 3 A-'])
            s.erode_iterations = int(self._values_extra['-SLIDER WINDOW 3 B-'])
            s.blur_threshold_A = int(self._values_extra['-SLIDER WINDOW 4 A-'])
            s.blur_threshold_B = int(self._values_extra['-SLIDER WINDOW 4 B-'])
        elif s.edge_detection_type == 3:
            s.blob_threshold_A = self._values_extra['-SLIDER WINDOW 2 A-']
            s.blob_threshold_B = self._values_extra['-SLIDER WINDOW 2 B-']
            s.canny_threshold_A = self._values_extra['-SLIDER WINDOW 3 A-']
            s.canny_threshold_B = self._values_extra['-SLIDER WINDOW 3 B-']
            # TODO: add iteration control to dilate en erode
        elif s.edge_detection_type == 0:
            s.canny_threshold_A = self._values_extra['-SLIDER WINDOW 2 A-']
            s.canny_threshold_B = self._values_extra['-SLIDER WINDOW 2 B-']

    def _update_extra_layout(self, s) -> bool:
        """
        Changes the layout of the extra window
        :param s: Settings object used to check edge_detecion_type for which layout needed
        :type s: Settings
        :return: True if it needs updating
        :return: False if ti doesn't need updating
        :rtype: bool
        """
        if self._values['-DETECTION TYPE-'] == 'Threshold Detection' and s.edge_detection_type != 1:
            s.edge_detection_type = 1
            self._extra_window['-DETECTION TYPE TEXT-'].update(value='Threshold Detection')
            self._extra_window['-WINDOW 1 TEXT-'].update(value='Grayscale View', visible=True)
            self._extra_window['-WINDOW 2 TEXT-'].update(value='Contour View', visible=True)
            self._extra_window['-WINDOW 3 TEXT-'].update(visible=False)
            self._extra_window['-WINDOW 4 TEXT-'].update(visible=False)
            self._extra_window['-WINDOW 1-'].update(visible=True)
            self._extra_window['-WINDOW 2-'].update(visible=True)
            self._extra_window['-WINDOW 3-'].update(visible=False)
            self._extra_window['-WINDOW 4-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 1 A-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 1 B-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 2 A-'].update(range=(0, 255), value=s.contour_threshold_A,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 2 B-'].update(range=(0, 255), value=s.contour_threshold_B,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 3 A-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 3 B-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 4 A-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 4 B-'].update(visible=False)
            self._extra_window['-RADIO ERODE-'].update(visible=False)
            self._extra_window['-RADIO DILATE-'].update(visible=False)
            self._extra_window['-RADIO CANNY-'].update(visible=False)
            self._extra_window['-RADIO THRESHOLD-'].update(visible=False)
            return True
        elif self._values['-DETECTION TYPE-'] == 'Canny + Threshold' and s.edge_detection_type != 2:
            s.edge_detection_type = 2
            self._extra_window['-DETECTION TYPE TEXT-'].update(value='Canny + Threshold Detection')
            self._extra_window['-WINDOW 1 TEXT-'].update(value='Grayscale View', visible=True)
            self._extra_window['-WINDOW 2 TEXT-'].update(value='Canny View', visible=True)
            self._extra_window['-WINDOW 3 TEXT-'].update(value='Erode View', visible=True)
            self._extra_window['-WINDOW 4 TEXT-'].update(value='Blur View', visible=True)
            self._extra_window['-WINDOW 1-'].update(visible=True)
            self._extra_window['-WINDOW 2-'].update(visible=True)
            self._extra_window['-WINDOW 3-'].update(visible=True)
            self._extra_window['-WINDOW 4-'].update(visible=True)
            self._extra_window['-SLIDER WINDOW 1 A-'].update(range=(0, 255), value=s.contour_threshold_A,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 1 B-'].update(range=(0, 255), value=s.contour_threshold_B,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 2 A-'].update(range=(0, 255), value=s.canny_threshold_A,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 2 B-'].update(range=(0, 255), value=s.canny_threshold_B,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 3 A-'].update(range=(1, 10), value=s.dilate_iterations,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 3 B-'].update(range=(1, 10), value=s.erode_iterations,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 4 A-'].update(range=(1, 50), value=s.blur_threshold_A,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 4 B-'].update(range=(1, 50), value=s.blur_threshold_B,
                                                             visible=True)
            self._extra_window['-RADIO ERODE-'].update(visible=True)
            self._extra_window['-RADIO DILATE-'].update(visible=True)
            self._extra_window['-RADIO CANNY-'].update(visible=True)
            self._extra_window['-RADIO THRESHOLD-'].update(visible=True)
            return True
        elif self._values['-DETECTION TYPE-'] == 'Blob + Canny' and s.edge_detection_type != 3:
            s.edge_detection_type = 3
            self._extra_window['-DETECTION TYPE TEXT-'].update(value='Blob + Canny Detection')
            self._extra_window['-WINDOW 1 TEXT-'].update(value='Grayscale View', visible=True)
            self._extra_window['-WINDOW 2 TEXT-'].update(value='Blob View', visible=True)
            self._extra_window['-WINDOW 3 TEXT-'].update(value='Canny View', visible=True)
            self._extra_window['-WINDOW 4 TEXT-'].update(value='Dilate view', visible=True)
            self._extra_window['-WINDOW 1-'].update(visible=True)
            self._extra_window['-WINDOW 2-'].update(visible=True)
            self._extra_window['-WINDOW 3-'].update(visible=True)
            self._extra_window['-WINDOW 4-'].update(visible=True)
            self._extra_window['-SLIDER WINDOW 1 A-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 1 B-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 2 A-'].update(range=(0, 255), value=s.blob_threshold_A,
                                                             visible=False)
            self._extra_window['-SLIDER WINDOW 2 B-'].update(range=(0, 255), value=s.blob_threshold_B,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 3 A-'].update(range=(0, 255), value=s.canny_threshold_A,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 3 B-'].update(range=(0, 255), value=s.canny_threshold_B,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 4 A-'].update(range=(0, 255), value=s.canny_threshold_A,
                                                             # TODO: Update slider
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 4 B-'].update(range=(0, 255), value=s.canny_threshold_B,
                                                             # TODO: Update slider
                                                             visible=True)
            self._extra_window['-RADIO ERODE-'].update(visible=False)
            self._extra_window['-RADIO DILATE-'].update(visible=False)
            self._extra_window['-RADIO CANNY-'].update(visible=False)
            self._extra_window['-RADIO THRESHOLD-'].update(visible=False)
            return True
        elif self._values['-DETECTION TYPE-'] == 'Canny Detection' and s.edge_detection_type != 0:
            s.edge_detection_type = 0
            self._extra_window['-DETECTION TYPE TEXT-'].update(value='Canny Detection')
            self._extra_window['-WINDOW 1 TEXT-'].update(value='Grayscale View', visible=True)
            self._extra_window['-WINDOW 2 TEXT-'].update(value='Canny View', visible=True)
            self._extra_window['-WINDOW 3 TEXT-'].update(value='Lines view', visible=True)
            self._extra_window['-WINDOW 4 TEXT-'].update(visible=False)
            self._extra_window['-WINDOW 1-'].update(visible=True)
            self._extra_window['-WINDOW 2-'].update(visible=True)
            self._extra_window['-WINDOW 3-'].update(visible=True)
            self._extra_window['-WINDOW 4-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 1 A-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 1 B-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 2 A-'].update(range=(0, 255), value=s.canny_threshold_A,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 2 B-'].update(range=(0, 255), value=s.canny_threshold_B,
                                                             visible=True)
            self._extra_window['-SLIDER WINDOW 3 A-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 3 B-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 4 A-'].update(visible=False)
            self._extra_window['-SLIDER WINDOW 4 B-'].update(visible=False)
            self._extra_window['-RADIO ERODE-'].update(visible=False)
            self._extra_window['-RADIO DILATE-'].update(visible=False)
            self._extra_window['-RADIO CANNY-'].update(visible=False)
            self._extra_window['-RADIO THRESHOLD-'].update(visible=False)
            return True
        else:
            return False

    def _update_img(self, s: Settings, v: Video) -> None:
        """
        Updates the images used in the main window
        :param s: Settings used for image height and image width
        :type s: Settings
        :param v: Video object with the needed frames
        :type v: Video
        :return: None
        :rtype: None
        """
        normal_view = cv.resize(v.frame, (s.image_width, s.image_height))
        output_view = cv.resize(v.video_output, (s.image_width, s.image_height))
        imgbytes_normal = cv.imencode('.png', normal_view)[1].tobytes()
        imgbytes_output = cv.imencode('.png', output_view)[1].tobytes()
        self._window['-IMAGE NORMAL-'].update(data=imgbytes_normal, size=(s.image_width, s.image_height))
        self._window['-IMAGE OUTPUT-'].update(data=imgbytes_output, size=(s.image_width, s.image_height))

    def _update_extra_img(self, s: Settings, v: Video):
        """
        Updates the images used in the detection window
        :param s: Settings used for image height and image width
        :type s: Settings
        :param v: Video object with the needed frames
        :type v: Video
        :return: None
        :rtype: None
        """
        if s.edge_detection_type == 1:
            window2_view = cv.resize(v.thrash, (s.image_width, s.image_height))
        elif s.edge_detection_type == 2:
            if self._values_extra['-RADIO CANNY-']:
                window2_view = cv.resize(v.canny, (s.image_width, s.image_height))
                self._extra_window['-WINDOW 2 TEXT-'].update(value='Canny view')
            else:
                window2_view = cv.resize(v.thrash, (s.image_width, s.image_height))
                self._extra_window['-WINDOW 2 TEXT-'].update(value='Threshold view')
            if self._values_extra['-RADIO ERODE-']:
                window3_view = cv.resize(v.erode, (s.image_width, s.image_height))
                self._extra_window['-WINDOW 3 TEXT-'].update(value='Erode view')
            else:
                window3_view = cv.resize(v.dilate, (s.image_width, s.image_height))
                self._extra_window['-WINDOW 3 TEXT-'].update(value='Dilate view')

            window4_view = cv.resize(v.blur, (s.image_width, s.image_height))
        elif s.edge_detection_type == 3:
            window2_view = cv.resize(v.blob, (s.image_width, s.image_height))
            window3_view = cv.resize(v.canny, (s.image_width, s.image_height))
            window4_view = cv.resize(v.dilate, (s.image_width, s.image_height))
        elif s.edge_detection_type == 0:
            window2_view = cv.resize(v.canny, (s.image_width, s.image_height))
        else:
            window2_view = None
            window3_view = None

        window1_view = cv.resize(v.grayscale, (s.image_width, s.image_height))
        imgbytes_grayscale = cv.imencode('.png', window1_view)[1].tobytes()
        imgbytes_window2 = cv.imencode('.png', window2_view)[1].tobytes()
        self._extra_window['-WINDOW 1-'].update(data=imgbytes_grayscale, size=(s.image_width, s.image_height))
        self._extra_window['-WINDOW 2-'].update(data=imgbytes_window2, size=(s.image_width, s.image_height))
        if s.edge_detection_type > 1:
            imgbytes_window3 = cv.imencode('.png', window3_view)[1].tobytes()
            self._extra_window['-WINDOW 3-'].update(data=imgbytes_window3, size=(s.image_width, s.image_height))
            imgbytes_window4 = cv.imencode('.png', window4_view)[1].tobytes()
            self._extra_window['-WINDOW 4-'].update(data=imgbytes_window4, size=(s.image_width, s.image_height))

    def del_extra_window(self) -> None:
        """
        Cleans up the created extra window
        :return: None
        :rtype: None
        """
        self._extra_window.close()
        self._extra_window_bool = False
        self._extra_window = None
        self.extra_layout = None

    def __del__(self) -> int:
        """
        Cleans up the main window
        :return: 0
        """
        self._window.close()
        if self._extra_window is not None:
            self._extra_window.close()
        return 0
