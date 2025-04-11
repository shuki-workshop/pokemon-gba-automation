#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand
from Commands.PythonCommandBase import ImageProcPythonCommand
from logging import getLogger, DEBUG, NullHandler
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
from obswebsocket import obsws, requests
import csv
import threading
import pyautogui

# shiny_Feebas
# 色違いヒンバス自動化
#
# 前提条件
# - ボロの釣り竿をSELECT登録
# - 2匹目の1番上の技が「そらをとぶ」
# - 手持ちに「なみのり」を覚えたポケモンがいる
# - 「たきのぼり」は使用しない(超低確率でたきのぼりが必要なポイントのみにヒンバスがいる可能性あり)
# - ヒワマキシティに行ったことがある
# - 野生ポケモンから逃げられるすばやさもしくは複数回の試行に耐えられる体力がある

class shiny_Feebas(ImageProcPythonCommand):
    NAME = '色違いヒンバス自動化'

    def __init__(self, cam):
        super().__init__(cam)

        # 自動化設定============================================================================

        # ヒンバスがいないポイントだと判断するまでのハズレ回数
        self.JudgThreshold = 6

        # 1度ヒンバスが釣れたポイントでポイントが変更されたと判断するまでのハズレ回数
        self.TimeThreshold = 26

        # 画像認識の一致判定の閾値
        self.ImgThreshold = 0.96

        # 釣りポイントの移動ルートCSVファイル
        self.FishPointCsv = './Template/shiny_Feebus/route.csv'

        # カウンター初期値
        self.FishCount = 0

        # 開始位置(行番号)
        self.StartNum = 0

        # Reload Portボタンの座標
        self.reroadPortX = -1598
        self.reroadPortY = 843

        # Reload Portボタンを押す間隔
        self.reloadPortInterval = 60 * 20

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

        # ヒンバス文字
        self.ImgFeebasTxt = 'shiny_Feebus/349_txt.png'

        # ヒンバス画像
        self.ImgFeebasImg = 'shiny_Feebus/349_img.png'

        # 色違いヒンバス画像
        self.ImgFeebasShinyImg = 'shiny_Feebus/349_img_shiny.png'

        # コイキング文字
        self.ImgMagikarpTxt = 'shiny_Feebus/129_txt.png'

        # コイキング画像
        self.ImgMagikarpImg = 'shiny_Feebus/129_img.png'

        # 色違いコイキング画像
        self.ImgMagikarpShinyImg = 'shiny_Feebus/129_img_shiny.png'

        # メノクラゲ文字
        self.ImgTentacoolTxt = 'shiny_Feebus/072_txt.png'

        # メノクラゲ画像
        self.ImgTentacoolImg = 'shiny_Feebus/072_img.png'

        # ひいてる
        self.ImgHook = 'shiny_Feebus/Hook.png'

        # つりあげた
        self.ImgLandSuccess = 'shiny_Feebus/LandSuccess.png'

        # 逃げられた
        self.ImgLandFaild = 'shiny_Feebus/LandFaild.png'

        # つれないなぁ
        self.ImgNoCatches = 'shiny_Feebus/NoCatches.png'

        # 戦闘
        self.ImgBattle = 'shiny_Feebus/Battle.png'

        # コマンド
        self.ImgCmdBattle = 'shiny_Feebus/Cmd_battle.png'
        self.ImgCmdPokemon = 'shiny_Feebus/Cmd_Pokemon.png'
        self.ImgCmdBag = 'shiny_Feebus/Cmd_bag.png'
        self.ImgCmdEscape = 'shiny_Feebus/Cmd_escape.png'

        # にげる成功
        self.ImgEscapeSuccess = 'shiny_Feebus/EscapeSuccess.png'

        # ポケナビ
        self.ImgNavi = 'shiny_Feebus/pokenavi.png'

        # メニュー(ポケモン)
        self.ImgMenuPokemon = 'shiny_Feebus/pokemon.png'

        # ===================================================================================

        # 変数初期化
        self.JudgCount1 = 0
        self.JudgCount2 = 0
        self.RouteNum = 0
        self.dir = 'l'

        # ログ設定
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        # CSVファイル読み込み
        self.FishPoint = []
        with open(self.FishPointCsv, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.FishPoint.append(row)

        # OBS接続
        self.ws = obsws(self.obs_host, self.obs_port, self.obs_password)
        self.ws.connect()
        self.OBS_SET(self.FishCount)

        # 録画開始
        self.ws.call(requests.StartRecord())


    def do(self):
        print("shiny_Feebas_START")

        self.REROAD_PORT()

        # 初期位置へ移動
        print(self.RouteNum)
        self.MOVE(self.FishPoint[self.RouteNum])
        self.RouteNum += 1

        while True:
            if self.RouteNum <= self.StartNum:
                self.JudgCount1 = self.JudgThreshold
                self.result = ""
            else:
                self.result = self.FISHING()

            # 色違いが出たら終了
            if self.result == 'Shiny':
                break

            # ポイント判定
            if self.JudgCount1 == -1:
            # ヒンバスポイント
                self._logger.debug("This point")
            elif self.JudgCount1 == -1 and self.JudgCount2 > self.TimeThreshold:
            # ヒンバスポイントが変わった
                self._logger.debug("Change point")
                self.JudgCount1 = 0
                self.JudgCount2 = 0
                self.MOVE(self.FishPoint[0])
                self.RouteNum = 1
            elif self.JudgCount1 < self.JudgThreshold:
            # まだわからない
                self._logger.debug("Not judged")
            else:
            # ヒンバスポイントじゃない
                self._logger.debug("Judged")
                self.JudgCount1 = 0

                # 移動
                print(self.RouteNum)
                self.MOVE(self.FishPoint[self.RouteNum])
                self.RouteNum += 1
                if self.RouteNum >= len(self.FishPoint):
                    self.RouteNum = 0

        self.CREAN_UP()   


    # 釣り
    def FISHING(self):
        print("FISHING_START")

        while True:
            # つりざおを振る
            fish = False
            self.press(Button.Y, wait=0.2)
            while True:
                # ひいてるひいてる
                if self.isContainTemplate(self.ImgHook,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                    self.press(Button.A, wait=0.2)
                # つれないなあ
                elif self.isContainTemplate(self.ImgNoCatches,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                    self.wait(0.5)
                    self.press(Button.A)
                    break
                # 釣り上げた
                elif self.isContainTemplate(self.ImgLandSuccess,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                    self.press(Button.A, wait=1.0)
                    print("FISHED")
                    self.FishCount += 1
                    self.OBS_SET(self.FishCount)
                    result = self.BATTLE()
                    return result
                # 逃げられてしまった
                elif self.isContainTemplate(self.ImgLandFaild,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                    self.wait(0.5)
                    self.press(Button.A, wait=0.2)
                    break
                

    # 戦闘
    def BATTLE(self):
        print("BATTLE_START")
        self.wait(6.0)
        self.press(Button.A, wait=4.0)
        self.camera.saveCapture(str(self.FishCount))
        
        if self.isContainTemplate(self.ImgFeebasShinyImg,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            return 'Shiny'
        elif self.isContainTemplate(self.ImgFeebasTxt,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            if self.isContainTemplate(self.ImgFeebasImg,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            # 通常ヒンバス
                self.JudgCount1 = -1
                self.JudgCount2 = 0
                self.ESCAPE()
                return 'Escape'
            else:
            # 色違いヒンバス
                return 'Shiny'
        if self.isContainTemplate(self.ImgMagikarpShinyImg,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            return 'Shiny'
        elif self.isContainTemplate(self.ImgMagikarpTxt,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            if self.isContainTemplate(self.ImgMagikarpImg,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            # 通常コイキング
                if self.JudgCount1 == -1:
                    self.JudgCount2 += 1
                else:
                    self.JudgCount1 += 1
                self.ESCAPE()
                return 'Escape'
            else:
            # 色違いコイキング
                return 'Shiny'
        elif self.isContainTemplate(self.ImgTentacoolTxt,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            if self.isContainTemplate(self.ImgTentacoolImg,threshold=self.ImgThreshold, use_gray=False, show_value=True):
            # 通常メノクラゲ
                if self.JudgCount1 == -1:
                    self.JudgCount2 += 1
                else:
                    self.JudgCount1 += 1
                self.ESCAPE()
                return 'Escape'
            else:
            # 色違いメノクラゲ
                return 'Shiny'
        else:
            self.ESCAPE()
            return 'Escape'


    # 逃げる
    def ESCAPE(self):
        print("ESCAPE_START")
        while True:
            if self.isContainTemplate(self.ImgEscapeSuccess,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                self.press(Button.A, wait=3.0)
                break
            elif self.isContainTemplate(self.ImgCmdEscape,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                self.press(Button.A, wait=2.0)
            elif self.isContainTemplate(self.ImgCmdBattle,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                self.press(Direction.RIGHT, wait=0.3, duration=0.2)
            elif self.isContainTemplate(self.ImgCmdBag,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                self.press(Direction.DOWN, wait=0.3, duration=0.2)
            elif self.isContainTemplate(self.ImgCmdPokemon,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                self.press(Direction.RIGHT, wait=0.3, duration=0.2)
            else:
                self.press(Button.A, wait=2.0)


    # 移動
    def MOVE(self, moveList):
        print("MOVE_START")

        for move in moveList:
            if move == 'A':
                print('A')
                self.press(Button.A, wait=3.0)
            elif move == 'U' and self.dir != 'u':
                print('U')
                self.press(Direction.UP, wait=0.3, duration=0.2)
                self.dir = 'u'
            elif move == 'D' and self.dir != 'd':
                print('D')
                self.press(Direction.DOWN, wait=0.3, duration=0.2)
                self.dir = 'd'
            elif move == 'L' and self.dir != 'l':
                print('L')
                self.press(Direction.LEFT, wait=0.3, duration=0.2)
                self.dir = 'l'
            elif move == 'R' and self.dir != 'r':
                print('R')
                self.press(Direction.RIGHT, wait=0.3, duration=0.2)
                self.dir = 'r'
            elif move == 'u' or move == 'U':
                print('u')
                self.press(Direction.UP, wait=0.3, duration=0.05)
                self.dir = 'u'
            elif move == 'd' or move == 'D':
                print('d')
                self.press(Direction.DOWN, wait=0.3, duration=0.05)
                self.dir = 'd'
            elif move == 'l' or move == 'L':
                print('l')
                self.press(Direction.LEFT, wait=0.3, duration=0.05)
                self.dir = 'l'
            elif move == 'r' or move == 'R':
                print('r')
                self.press(Direction.RIGHT, wait=0.3, duration=0.05)
                self.dir = 'r'
            elif move == 'F':
                print('F')
                self.press(Button.PLUS, wait=1)
                while True:
                    if self.isContainTemplate(self.ImgMenuPokemon,threshold=0.9, use_gray=False, show_value=True):
                        self.press(Button.A, wait=2)
                        self.press(Direction.DOWN, wait=0.3, duration=0.05)
                        self.press(Button.A, wait=1)
                        self.press(Direction.DOWN, wait=0.3, duration=0.05)
                        self.press(Button.A, wait=2)
                        self.press(Direction.UP, wait=0.3, duration=0.5)
                        self.press(Direction.RIGHT, wait=0.3, duration=0.05)
                        self.press(Button.A, wait=7)
                        break
                    self.press(Direction.DOWN, wait=0.3, duration=0.05)
                self.dir = 'd'    

            if self.isContainTemplate(self.ImgNavi,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                while True:
                    self.press(Button.A, wait=1.0)
                    if not self.isContainTemplate(self.ImgNavi,threshold=self.ImgThreshold, use_gray=False, show_value=True):
                        self.wait(1.0)
                        break

            
            #if self.STATUS_RECOGNITON() == 'Battle':
            #    self.ESCAPE()
        self.camera.saveCapture()
    

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
        self.ws.call(requests.StopRecord())
        self.ws.disconnect()