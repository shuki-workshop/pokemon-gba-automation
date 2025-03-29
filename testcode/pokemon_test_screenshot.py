#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import ImageProcPythonCommand


class ScreenShot(ImageProcPythonCommand):
    NAME = '●スクショ取得'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        for i in range(100):
            self.camera.saveCapture(str(i))

