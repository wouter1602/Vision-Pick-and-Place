import PySimpleGUI as sg
from settings import Settings


class Ui:
    def __init__(self):
        self.layout = [[sg.Text('Some text')],
                       [sg.Text('Some other text:'), sg.InputText()],
                       [sg.Button('ok'), sg.Button('Cancel')]]

        self.window = sg.Window('Tes window', self.layout)
        self.event = None
        self.values = None

    def update(self, s: Settings) -> int:
        self.event, self.values = self.window.read()

        if self.event == sg.WIN_CLOSED or self.event == 'Cancel':
            return -1
        if s.verbose:
            print('You entered ', self.values[0])
        return 0

    def __del__(self) -> int:
        self.window.close()
        return 0
