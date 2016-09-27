#!/usr/bin/env python

"""
Hecto -- KiloエディタをPythonで書きなおしてみる試み
"""

import sys, os

HECTO_VERSION = "0.0.1"
HL_HIGHLIGHT_STRINGS = bin(1<<0)
HL_HIGHLIGHT_NUMBERS = bin(1<<1)
# シンタックスハイライトDB
HLDB = [
    {
        # C/C++
        'extensions': ['c', 'cpp'],
        'keywords': [
            # A few C/C++ keywords
            'switch', 'if', 'while', 'for', 'break', 'continue', 'return', 
            'else', 'struct', 'union', 'typedef', 'static', 'enum', 'class',
            # C types
            'int|', 'long|', 'double|', 'float|', 'char|', 'unsigned|',
            'signed|', 'void|',
        ],
        'singleline_comment_start': '//',
        'multiline_comment_start': '/*',
        'multiline_comment_end': '*/',
        'flags': HL_HIGHLIGHT_STRINGS | HL_HIGHLIGHT_NUMBERS,
    }
]


class EditorRow:
    def __init__(self):
        self.index
        self.size
        self.rsize
        self.chars
        self.render
        self.hl
        self.hl_oc


class Editor:
    def __init__(self):
        # Editor config
        self.cursor_x = 0       # 文字の中のカーソルのx,y位置
        self.cursor_y = 0       # 同上
        self.rowoff = 0         # 行のオフセットを表示
        self.coloff = 0         # 列のオフセットを表示
        self.numrows = 0        # 行の数
        self.is_rawmode = False # 端末が書き込みを許可しているか?
        self.row = []           # 行
        self.dirty = 0          # 編集されたが保存されていないか?
        self.filename = ""      # 現在開いているファイル名
        self.statusmsg = ""
        self.statusmsg_time
        self.syntax             # 現在のシンタックスハイライト
        
        # 端末のサイズを取得
        try:
            self.screencols, self.screenrows = os.get_terminal_size()
        except OSError as e:
            print("Unable to query the screen for size (columns / rows)", e)
            sys.exit()
        self.screenrows -= 2    # ステータスバーの空き確保

    def select_syntax_highlight(self, filename):
        """ ファイル名からシンタックスハイライトスキームを選択する """
        extension = filename.split(".")[-1]    # 拡張子を取得
        for hl in HLDB:
            if extension in hl['extentions']:
                self.syntax = hl
                return

    def open(self, filename):
        """ 指定されたプログラムをエディタのメモリにロードする """
        self.dirty = 0
        self.filename = filename

        with open(filename, "r") as f:
            lines = f.readlines()

        for line in lines:
            if len(line) and (line[-1] == '\n' or line[-1] == '\r'):
                pass    # 何のため?
            self.insert_row(self.numrows, line)
        self.dirty = 0

    def insert_row(self, at, row):
        """ 指定された位置に行を挿入する """
        if (at > self.numrows):
            return
        if at != self.numrows:
            pass
        self.row.append(EditorRow())
        self.row[at].size = len(line)
        self.row[at].chars = row
        self.row[at].hl = None
        self.row[at].ho_oc = 0
        self.row[at].render = None
        self.row[at].rsize = 0
        self.row[at].index = at
        self.update_row()
        self.numrows += 1
        self.dirty += 1


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: hecto <filename>\n")
        sys.exit(1)

    editor = Editor()
    editor.select_syntax_highlight(sys.argv[1])
