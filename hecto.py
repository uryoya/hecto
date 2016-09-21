#!/usr/bin/env python3

"""
Hecto -- KiloエディタをPythonで書きなおしてみる試み
"""

HECTO_VERSION = "0.0.1"


class Editor:
    def __init__(self):
        # config
        self.cursor_x = 0   # 文字の中のカーソルのx,y位置
        self.cursor_y = 0   # 同上
        self.rowoff = 0     # 行のオフセットを表示
        self.coloff = 0     # 列のオフセットを表示
        self.screenrows = 0 # 表示できる行
        self.screencols = 0 # 表示できる列
        self.numrows = 0    # 
