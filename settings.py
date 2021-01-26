# Settings Json
import json
import os


class Settings:
    display_output: bool
    verbose: bool
    capture_device: str
    frame_width: int
    frame_height: int
    edge_detection_type: int
    canny_threshold_A: int
    canny_threshold_B: int
    blob_threshold_A: int
    blob_threshold_B: int
    blur_threshold_A: int
    blur_threshold_B: int
    dilate_iterations: int
    erode_iterations: int
    triangle_1: int
    triangle_2: int
    triangle_3: int
    triangle_4: int
    triangle_5: int
    square: int
    parallelogram: int
    TCP_IP: str
    TCP_PORT: int
    use_test_image: bool
    test_image: str
    autodetect: bool
    image_height: int
    image_width: int

    def __init__(self) -> None:
        # Get ABS path of settings file so it can be run outside of dir
        setting_file = os.path.dirname(__file__) + "/settings.json"
        try:
            self._json_obj = json.loads(open(setting_file).read())
        except OSError:
            print("Json does not exist \nCreating Json")
            if self.__create_json() != 0:
                pass

        self.verbose = self._json_obj['verbose']
        self.capture_device = self._json_obj['capture_device']
        self.frame_width = self._json_obj['webcam_settings']['frame_width']
        self.frame_height = self._json_obj['webcam_settings']['frame_height']
        self.edge_detection_type = self._json_obj['detection_settings']['edge_detection_type']
        self.canny_threshold_A = self._json_obj['detection_settings']['canny_threshold_A']
        self.canny_threshold_B = self._json_obj['detection_settings']['canny_threshold_B']
        self.contour_threshold_A = self._json_obj['detection_settings']['contour_threshold_A']
        self.contour_threshold_B = self._json_obj['detection_settings']['contour_threshold_B']
        self.blob_threshold_A = self._json_obj['detection_settings']['blob_threshold_A']
        self.blob_threshold_B = self._json_obj['detection_settings']['blob_threshold_B']
        self.blur_threshold_A = self._json_obj['detection_settings']['blur_threshold_A']
        self.blur_threshold_B = self._json_obj['detection_settings']['blur_threshold_B']
        self.dilate_iterations = self._json_obj['detection_settings']['dilate_iterations']
        self.erode_iterations = self._json_obj['detection_settings']['erode_iterations']
        self.triangle_1 = self._json_obj['block_colours']['triangle_1']
        self.triangle_2 = self._json_obj['block_colours']['triangle_2']
        self.triangle_3 = self._json_obj['block_colours']['triangle_3']
        self.triangle_4 = self._json_obj['block_colours']['triangle_4']
        self.triangle_5 = self._json_obj['block_colours']['triangle_5']
        self.square = self._json_obj['block_colours']['square']
        self.parallelogram = self._json_obj['block_colours']['parallelogram']
        self.contour_poly_threshold = self._json_obj['detection_settings']['contour_poly_threshold']
        self.TCP_IP = self._json_obj['connection']['TCP_IP']
        self.TCP_PORT = self._json_obj['connection']['TCP_PORT']
        self.use_test_image = self._json_obj['use_test_image']
        self.test_image = self._json_obj['test_image']
        self.display_output = self._json_obj['display_output']['enable']
        self.image_height = self._json_obj['display_output']['image_height']
        self.image_width = self._json_obj['display_output']['image_width']
        self.autodetect = self._json_obj['display_output']['autodetect']

    def __create_json(self) -> int:
        self._json_obj = {
            'verbose': False,
            'capture_device': "/dev/video0",
            'webcam_settings': {
                'frame_width': 2000,
                'frame_height': 2000
            },
            'detection_settings': {
                'edge_detection_type': 0,
                'canny_threshold_A': 100,
                'canny_threshold_B': 100,
                'contour_threshold_A': 100,
                'contour_threshold_B': 255,
                'blob_threshold_A': 255,
                'blob_threshold_B': 255,
                'blur_threshold_A': 10,
                'blur_threshold_B': 10,
                'contour_poly_threshold': 0.01
            },
            'block_colours': {
                'triangle_1': 0xFFFFFF,
                'triangle_2': 0xFFFFFF,
                'triangle_3': 0xFFFFFF,
                'triangle_4': 0xFFFFFF,
                'triangle_5': 0xFFFFFF,
                'square': 0xFFFFFF,
                'parallelogram': 0xFFFFFF
            },
            'connection': {
                'TCP_IP': '127.0.0.1',
                'TCP_PORT': 5000,
            },
            'use_test_image': False,
            'test_image': "./Image/Test_Img_Resized.jpg",
            'display_output': {
                'enable': False,
                'image_height': 360,
                'image_width': 480,
                'autodetect': False
            },
        }

        return self.save_jason()

    def update_json(self) -> int:
        self._json_obj['verbose'] = self.verbose
        self._json_obj['capture_device'] = self.capture_device
        self._json_obj['webcam_settings']['frame_width'] = self.frame_width
        self._json_obj['webcam_settings']['frame_height'] = self.frame_height

        self._json_obj['detection_settings']['edge_detection_type'] = self.edge_detection_type
        self._json_obj['detection_settings']['canny_threshold_A'] = self.canny_threshold_A
        self._json_obj['detection_settings']['canny_threshold_B'] = self.canny_threshold_B
        self._json_obj['detection_settings']['contour_threshold_A'] = self.contour_threshold_A
        self._json_obj['detection_settings']['contour_threshold_B'] = self.contour_threshold_B
        self._json_obj['detection_settings']['contour_poly_threshold'] = self.contour_poly_threshold
        self._json_obj['detection_settings']['blob_threshold_A'] = self.blob_threshold_A
        self._json_obj['detection_settings']['blob_threshold_B'] = self.blob_threshold_B
        self._json_obj['detection_settings']['blur_threshold_A'] = self.blur_threshold_A
        self._json_obj['detection_settings']['blur_threshold_B'] = self.blur_threshold_B
        self._json_obj['detection_settings']['dilate_iterations'] = self.dilate_iterations
        self._json_obj['detection_settings']['erode_iterations'] = self.erode_iterations

        self._json_obj['block_colours']['triangle_1'] = self.triangle_1
        self._json_obj['block_colours']['triangle_2'] = self.triangle_2
        self._json_obj['block_colours']['triangle_3'] = self.triangle_3
        self._json_obj['block_colours']['triangle_4'] = self.triangle_4
        self._json_obj['block_colours']['triangle_5'] = self.triangle_5
        self._json_obj['block_colours']['square'] = self.square
        self._json_obj['block_colours']['parallelogram'] = self.parallelogram

        self._json_obj['connection']['TCP_IP'] = self.TCP_IP
        self._json_obj['connection']['TCP_PORT'] = self.TCP_PORT

        self._json_obj['use_test_image'] = self.use_test_image
        self._json_obj['test_image'] = self.test_image

        self._json_obj['display_output']['enable'] = self.display_output
        self._json_obj['display_output']['image_height'] = self.image_height
        self._json_obj['display_output']['image_width'] = self.image_width
        self._json_obj['display_output']['autodetect'] = self.autodetect
        return self.save_jason()

    def save_jason(self) -> int:
        try:
            with open('./settings.json', 'w') as jsonFile:
                json.dump(self._json_obj, jsonFile, indent=4)
        except OSError:
            if self.verbose:
                print("Can't create \'settings.json\' file")
            return -2
        return 0

    def __del__(self) -> int:
        if self.verbose:
            print("Closing Settings file")
        if self.update_json() != 0:
            return -2
        self._json_obj = None
        return 0
