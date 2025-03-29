#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick, Hat
import csv

class check(ImageProcPythonCommand):
    NAME = '●CSV&移動テスト'

    def __init__(self,cam):
        super().__init__(cam)

        self.RouteNum = 1
        self.dir='l'

        self.wait_a = 3
        self.wait_move = 1

        # 釣りポイントの移動ルートCSVファイル
        self.FishPointCsv = './Template/shiny_Feebus/route.csv'

        self.FishPoint = []
        with open(self.FishPointCsv, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.FishPoint.append(row)

    def do(self):
        while True:
            print(self.RouteNum+1)
            self.MOVE(self.FishPoint[self.RouteNum])
            self.RouteNum += 1

    def MOVE(self,moveList):
        self._logger.debug("MOVE_START")

        for move in moveList:
            self._logger.debug(move)

            if move == 'A':
                print('A')
                self.press(Button.A, wait=self.wait_a)
            elif move == 'U' and self.dir != 'u':
                print('U')
                self.press(Direction.UP, wait=self.wait_move, duration=0.2)
                self.dir = 'u'
            elif move == 'D' and self.dir != 'd':
                print('D')
                self.press(Direction.DOWN, wait=self.wait_move, duration=0.2)
                self.dir = 'd'
            elif move == 'L' and self.dir != 'l':
                print('L')
                self.press(Direction.LEFT, wait=self.wait_move, duration=0.2)
                self.dir = 'l'
            elif move == 'R' and self.dir != 'r':
                print('R')
                self.press(Direction.RIGHT, wait=self.wait_move, duration=0.2)
                self.dir = 'r'
            elif move == 'u' or move == 'U':
                print('u')
                self.press(Direction.UP, wait=self.wait_move, duration=0.05)
                self.dir = 'u'
            elif move == 'd' or move == 'D':
                print('d')
                self.press(Direction.DOWN, wait=self.wait_move, duration=0.05)
                self.dir = 'd'
            elif move == 'l' or move == 'L':
                print('l')
                self.press(Direction.LEFT, wait=self.wait_move, duration=0.05)
                self.dir = 'l'
            elif move == 'r' or move == 'R':
                print('r')
                self.press(Direction.RIGHT, wait=self.wait_move, duration=0.05)
                self.dir = 'r'

