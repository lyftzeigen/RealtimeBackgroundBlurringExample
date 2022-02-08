import BackgroundMatting

from PIL.ImageQt import ImageQt

from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import QtCore, QtWidgets

from design import MainForm


class FrmMain(QtWidgets.QMainWindow, MainForm.Ui_MainWindow):
    def __init__(self):
        super().__init__()        
        self.setupUi(self)
        self.capture = BackgroundMatting.ThreadedCapture()
        self.matter = BackgroundMatting.ThreadedBackgroundMatter()
        self.fps_counter = QtCore.QTimer()
        self.video_updater = QtCore.QTimer()
        self.video_source = 'none' or 'capture' or 'matting'
        self.connect()
        self.fps_counter.start(33)
        self.video_updater.start(33)

    def connect(self):
        self.btnStartCapture.clicked.connect(self.start_capture)
        self.btnSwitchDetection.clicked.connect(self.switch_detection)
        self.btnTakeBackground.clicked.connect(self.take_background)
        self.fps_counter.timeout.connect(self.update_fps)
        self.video_updater.timeout.connect(self.update_video)

    def start_capture(self):
        self.video_source = 'capture'
        self.btnStartCapture.setEnabled(False)
        self.btnSwitchDetection.setEnabled(True)
        self.btnTakeBackground.setEnabled(True)
        self.capture.start()

    def switch_detection(self):
        if self.video_source == 'capture':
            self.video_source = 'matting'
            self.btnSwitchDetection.setText('Stop detection')
            self.btnTakeBackground.setEnabled(False)
            self.matter.start()
        elif self.video_source == 'matting':
            self.video_source = 'capture'
            self.btnSwitchDetection.setText('Start detection')
            self.btnTakeBackground.setEnabled(True)
            self.matter.terminate()

    def take_background(self):
        self.matter.take_background()

    def stop_detection(self):
        self.matter.terminate()
        self.video_source = 'capture'
    
    def update_fps(self):
        self.setWindowTitle(
            f'Capture FPS: {self.capture.get_fps()}, ' +
            f'Matting FPS: {self.matter.get_fps()}')

    def update_video(self):
        if self.video_source == 'capture':
            frame = self.capture.get_rgb_frame()
        elif self.video_source == 'matting':
            frame = self.matter.get_matted_frame()
        else:
            return

        image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(image)
        self.lblVideo.setPixmap(pixmap)

    def closeEvent(self, event):
        self.matter.terminate()
        self.capture.terminate()
        self.fps_counter.stop()
        self.video_updater.stop()

