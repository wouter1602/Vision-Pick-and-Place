#
import json


class Settings:
    display_output: bool
    verbose: bool
    capture_device: str
    edge_detection_type: int
    edge_threshold: int
    TCP_IP: str
    TCP_PORT: int
    use_test_image: bool
    test_image: str

    def __init__(self) -> None:
        try:
            self.__json_obj = json.loads(open('./settings.json').read())
        except OSError:
            print("Json does not exist \nCreating Json")
            if self.__create_json() != 0:
                pass

        # Put json object in specific variables
        self.display_output = self.__json_obj['display_output']
        self.verbose = self.__json_obj['verbose']
        self.capture_device = self.__json_obj['capture_device']
        self.edge_detection_type = self.__json_obj['edge_detection_type']
        self.edge_threshold = self.__json_obj['edge_threshold']
        self.TCP_IP = self.__json_obj['TCP_IP']
        self.TCP_PORT = self.__json_obj['TCP_PORT']
        self.use_test_image = self.__json_obj['use_test_image']
        self.test_image = self.__json_obj['test_image']

    def __create_json(self) -> int:
        self.__json_obj = {'display_output': False, 'verbose': False, 'capture_device': "/dev/video1", 'edge_detection_type': 0,
                           'edge_threshold': 100, 'TCP_IP': '127.0.0.1', 'TCP_PORT': 5000, 'use_test_image': False,
                           'test_image': "Test_Img.jpg"}

        return self.update_json()

    def update_json(self) -> int:
        self.__json_obj['display_output'] = self.display_output
        self.__json_obj['verbose'] = self.verbose
        self.__json_obj['capture_device'] = self.capture_device
        self.__json_obj['edge_detection_type'] = self.edge_detection_type
        self.__json_obj['edge_threshold'] = self.edge_threshold
        self.__json_obj['TCP_IP'] = self.TCP_IP
        self.__json_obj['TCP_PORT'] = self.TCP_PORT
        self.__json_obj['use_test_image'] = self.use_test_image
        self.__json_obj['test_image'] = self.test_image

        try:
            with open('./settings.json', 'w') as jsonFile:
                json.dump(self.__json_obj, jsonFile, indent=4)
        except OSError:
            if self.verbose:
                print("Can't create \'settings.json\' file")
            return -2
        return 0

    def __del__(self) -> int:
        if self.update_json() != 0:
            return -2
        self.__json_obj = None
        return 0
