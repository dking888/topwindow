# -*- coding: utf-8 -*-
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['topwindow.py', '-w', '--icon=1.ico', '--add-data=icon.png;.']
    run(opts)