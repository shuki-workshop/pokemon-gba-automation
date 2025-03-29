#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat

class check(ImageProcPythonCommand):
    NAME = '●画像認識テスト'

    def __init__(self,cam):
        super().__init__(cam)
        self.wait_move = 1
        # 画像ファイル指定=====================================================================

        # ヒンバス
        self.ImgFeebas = 'shiny_Feebus/349.png'

        # 色違いヒンバス
        self.ImgFeebas_shiny = 'shiny_Feebus/349_shiny.png'

        # コイキング
        self.ImgMagikarp = 'shiny_Feebus/129.png'

        # 色違いコイキング
        self.ImgMagikarp_shiny = 'shiny_Feebus/129_shiny.png'

        # メノクラゲ
        self.ImgTentacool = 'shiny_Feebus/129_shiny.png'

        # 色違いメノクラゲ
        self.ImgTentacool_shiny = 'shiny_Feebus/129_shiny.png'

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

        # にげる成功
        self.ImgEscapeSuccess = 'shiny_Feebus/EscapeSuccess.png'

        # にげる失敗
        self.ImgEscapeFaild = 'shiny_Feebus/'

        # メニュー(ポケモン)
        self.ImgMenuPokemon = 'shiny_Feebus/pokemon.png'

        # メニュー(レポート)
        self.ImgMenuReport = 'shiny_Feebus/report.png'

        # ===================================================================================

    def do(self):
        #self.ALL_IMG_RECOG()
        #self.ONE_LOOP_IMG_RECOG()
        self.START_POINT()

        print("Check_END")

    def ALL_IMG_RECOG(self):
        print("●コイキング判定")
        if self.isContainTemplate(self.ImgMagikarp,threshold=0.8, use_gray=False, show_value=True):
            #----.png -> 判定したいファイル名を入れる
            #threshold=0.8 ->0.8以上の時True
            #use_gray=True ->白黒画像で判定 / use_gray=False ->カラーで判定
            #show_value=True ->判定時の数値を表示する / show_value=True ->判定時の数値を表示しない
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした")

        print("●色コイキング判定")
        if self.isContainTemplate(self.ImgMagikarp_shiny,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 

        print("●ヒンバス判定")
        if self.isContainTemplate(self.ImgFeebas,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした")

        print("●色ヒンバス判定")
        if self.isContainTemplate(self.ImgFeebas_shiny,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 

        print("●戦闘判定")
        if self.isContainTemplate(self.ImgBattle,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 

        print("●釣り上げた判定")
        if self.isContainTemplate(self.ImgLandSuccess,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 

        print("●つれない判定")
        if self.isContainTemplate(self.ImgNoCatches,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 

        print("●にげられ判定")
        if self.isContainTemplate(self.ImgLandFaild,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 

        print("●ひいてる判定")
        if self.isContainTemplate(self.ImgHook,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 

        print("●にげきれた判定")
        if self.isContainTemplate(self.ImgEscapeSuccess,threshold=0.8, use_gray=False, show_value=True):
            print("画像が一致しました")
        else:
            print("画像が一致しませんでした") 
        
    def ONE_LOOP_IMG_RECOG(self):
        while True:
            print("●ひいてる判定")
            if self.isContainTemplate(self.ImgHook,threshold=0.8, use_gray=False, show_value=True):
                print("画像が一致しました")
                break
            else:
                print("画像が一致しませんでした") 
                
    def START_POINT(self):
        self.press(Button.PLUS, wait=1)
        while True:
            self.press(Direction.DOWN, wait=self.wait_move, duration=0.05)
            if self.isContainTemplate(self.ImgMenuPokemon,threshold=0.9, use_gray=False, show_value=True):
                self.press(Button.A, wait=2)
                self.press(Direction.DOWN, wait=self.wait_move, duration=0.05)
                self.press(Button.A, wait=1)
                self.press(Direction.DOWN, wait=self.wait_move, duration=0.05)
                self.press(Button.A, wait=2)
                self.press(Direction.UP, wait=self.wait_move, duration=0.5)
                self.press(Direction.RIGHT, wait=self.wait_move, duration=0.05)
                self.press(Button.A, wait=7)
                self.press(Direction.LEFT, wait=self.wait_move, duration=0.2*22)
                self.press(Direction.DOWN, wait=self.wait_move, duration=0.2*24)
                self.press(Direction.LEFT, wait=self.wait_move, duration=0.2*1)
                self.press(Direction.DOWN, wait=self.wait_move, duration=0.2*7)
                self.press(Direction.LEFT, wait=self.wait_move, duration=0.2*4)
                self.press(Direction.DOWN, wait=self.wait_move, duration=0.2*16)
                break
