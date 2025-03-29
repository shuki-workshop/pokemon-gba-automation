#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
import csv
import atexit
from obswebsocket import obsws, requests



class check(ImageProcPythonCommand):
    NAME = '●OBS接続テスト'
    

    def __init__(self,cam):
        super().__init__(cam)

        # OBS設定=============================================================================
        self.obs_host = "localhost"
        self.obs_port = 4455
        self.obs_password = "ySeCxebljZ4zXtqP"
        #self.obs_password = "××××××××××××××××"

        self.obs_source = "num"
        # ===================================================================================

        self.i = 0

        self.ws = obsws(self.obs_host, self.obs_port, self.obs_password)
        self.ws.connect()

    def do(self):
        self.ws.call(requests.StartRecord())
        while True:
            settings = {"text":str(self.i).zfill(5)}
            response = self.ws.call(requests.SetInputSettings(inputName=self.obs_source, inputSettings=settings, overlay=False))
            self.i += 1
            self.wait(1)

            if self.i > 30:
                break
        self.ws.call(requests.StopRecord())
        self.ws.disconnect()

    def cleanup(self):
        print("プログラムが終了する前に実行されるクリーンアップ処理")
        self.ws.disconnect()
        print("websocket接続完了")

    atexit.register(cleanup)