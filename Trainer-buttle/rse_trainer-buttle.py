#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick
from obswebsocket import obsws, requests
import threading
import pyautogui

class check(ImageProcPythonCommand):
    NAME = 'トレーナー戦自動化'

    def __init__(self,cam):
        super().__init__(cam)

        # 自動化設定============================================================================

        # 画像認識の一致判定の閾値
        self.ImgThreshold = 0.9

        # カウンター初期値
        self.Count = 1

        # Reload Portボタンの座標
        self.reroadPortX = -1598
        self.reroadPortY = 843

        # Reload Portボタンを押す間隔
        self.reloadPortInterval = 60 * 10

        # ===================================================================================

        # OBS設定=============================================================================
        # サーバーIP (同一PCの場合は"localhost")
        self.obs_host = "localhost"

        # サーバーポート
        self.obs_port = 4455

        # サーバーパスワード
        self.obs_password = "××××××××××××××××"

        # 変更するソース名
        self.obs_source = "num"
        # ===================================================================================
    
        # 画像ファイル指定=====================================================================

        self.ImgWin = 'trainer-battle/win.png'
        self.ImgLose = 'trainer-battle/lose.png'

        # ===================================================================================

        # OBS接続
        self.ws = obsws(self.obs_host, self.obs_port, self.obs_password)
        self.ws.connect()
        self.OBS_SET(self.Count)

    def do(self):
        print("プログラム開始")

        self.REROAD_PORT()

        while True:
            self.press(Button.A, wait=1.0)
            #self.camera.saveCapture()
            if self.isContainTemplate(self.ImgWin,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                self.press(Button.A, wait=1.0)
                self.press(Button.A, wait=1.0)
                self.press(Button.A, wait=1.0)
                break
            elif self.isContainTemplate(self.ImgLose,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                self.Count += 1
                self.OBS_SET(self.Count)
                self.press(Button.ZR, wait=1.5)
                self.press(Button.A, wait=0.5)
                self.press(Direction.LEFT, wait=2.0, duration=0.2)
                self.press(Button.A, wait=1.0)
                self.press(Button.A, wait=10.0)
                self.press(Button.A, wait=2.0)
                self.press(Button.A, wait=2.0)
                self.press(Button.A, wait=3.0)
                self.press(Button.A, wait=2.0)
                #self.press(Direction.LEFT, wait=0.3, duration=0.2)
                #self.press(Direction.DOWN, wait=0.3, duration=0.2)
            
        self.CREAN_UP() 

    # 定期的に「Reload Port」ボタンを押す
    def REROAD_PORT(self):
        print("REROAD_PORT")
        pyautogui.click(self.reroadPortX, self.reroadPortY)
        threading.Timer(self.reloadPortInterval, self.REROAD_PORT).start()

    # OBSのカウンターを設定
    def OBS_SET(self,num):
        settings = {"text":str(num).zfill(5)}
        self.ws.call(requests.SetInputSettings(inputName=self.obs_source, inputSettings=settings, overlay=False))


    # 終了時の処理
    def CREAN_UP(self):
        threading.Timer(self.reloadPortInterval, self.REROAD_PORT).cancel()
        self.ws.disconnect()
