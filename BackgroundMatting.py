import os
import cv2
import time
import torch
import numpy as np

from PIL import Image

from torch.nn.functional import interpolate
from torchvision.transforms.functional import to_tensor, gaussian_blur

from PyQt6.QtCore import QThread


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class ThreadedCapture(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.is_running = False
        self.camera = None
        self.frame = None
        self.width = 640
        self.height = 480
        self.frames_timecodes = []

    def __del__(self):
        if self.is_running:
            self.wait()

    def run(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.camera.set(cv2.CAP_PROP_FOURCC,
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        self.is_running = True

        while self.is_running:
            # Do stuff
            _, self.frame = self.camera.read()

            # Collect frames timecodes
            self.frames_timecodes.append(time.time())
            self.frames_timecodes = sorted(self.frames_timecodes)
            self.frames_timecodes = self.frames_timecodes[-200:]

            # Do sleep
            QThread.msleep(0)

        self.camera.release()

    def terminate(self):
        self.is_running = False
        if self.camera:
            self.camera.release()

    def get_rgb_frame(self):
        if self.frame is not None:
            return self.frame[:, :, ::-1].copy()

        return np.zeros((self.height, self.width, 3), np.uint8)

    def get_fps(self):
        now = time.time()
        frames_in_last_second = [
            t for t in self.frames_timecodes if (now - t) <= 1]
        return len(frames_in_last_second)


class ThreadedBackgroundMatter(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.is_running = False
        self.capture = ThreadedCapture()

        # Processed frame
        self.frame = None

        # Background color
        self.background_color_tensor = torch.tensor(
            [0.5, 0.9, 0.4]).view((1, 3, 1, 1))

        # Load mobilenet model
        self.model = torch.jit.load(
            'data/torchscript_mobilenetv2_fp32.pth').eval()
        self.model.backbone_scale = 1/4
        self.model.refine_sample_pixels = 80_000

        # Initialize background
        if os.path.isfile('data/background.jpg'):
            self.background_tensor = Image.open('data/background.jpg')
        else:
            self.background_tensor = np.zeros(
                (self.capture.height, self.capture.width, 3), np.uint8)

        self.background_tensor = to_tensor(self.background_tensor)
        self.background_tensor = self.background_tensor.unsqueeze(0)

        self.frames_timecodes = []

    def __del__(self):
        if self.is_running:
            self.wait()

    def run(self):
        self.is_running = True

        while self.is_running:
            # Take frame
            frame = self.capture.get_rgb_frame()
            frame = to_tensor(frame).unsqueeze(0)

            # Detect foregraund and background
            pha, fgr = self.model(frame, self.background_tensor)[:2]

            # Resize, blur and backsize
            frame = interpolate(
                frame, (self.capture.height // 3, self.capture.width // 3))
            frame = gaussian_blur(frame, [9, 9])
            frame = interpolate(
                frame, (self.capture.height, self.capture.width))

            # Apply background bluring
            frame = pha * fgr  # + (1 - pha) * frame

            # Convert to np array of bytes
            frame = frame.squeeze(0).permute((1, 2, 0)).cpu().numpy()
            self.frame = (frame * 255).astype(np.uint8)

            # Collect frames timecodes
            self.frames_timecodes.append(time.time())
            self.frames_timecodes = sorted(self.frames_timecodes)
            self.frames_timecodes = self.frames_timecodes[-200:]

            # Do sleep
            QThread.msleep(0)

    def get_matted_frame(self):
        if self.frame is not None:
            return self.frame.copy()

        return np.zeros((self.capture.height, self.capture.width, 3), np.uint8)

    def take_background(self):
        background = self.capture.get_rgb_frame()

        # Cache background
        Image.fromarray(background).save('data/background.jpg')

        self.background_tensor = to_tensor(background)
        self.background_tensor = self.background_tensor.unsqueeze(0)

    def terminate(self):
        self.is_running = False

    def get_fps(self):
        now = time.time()
        frames_in_last_second = [
            t for t in self.frames_timecodes if (now - t) <= 1]

        return len(frames_in_last_second)
