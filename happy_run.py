import random

import win32clipboard
from win32api import *
from win32con import *
import time

# 依次经过的点的经纬度，百度地图查询：https://api.map.baidu.com/lbsapi/getpoint/index.html ，locationList内的内容可以随意增加
# 但是必须依次输入
locationList = ["105.584507,29.400744", "105.583752,29.401747", "105.582962,29.401346", "105.583689,29.400123"]
# 速度参数，数值越大速度越慢
speedIndex = 1

# 按下按键
def keyDown(keyNum):
    keybd_event(keyNum, 0, 0, 0)

# 松开按键
def keyUP(keyNum):
    keybd_event(keyNum, 0, KEYEVENTF_KEYUP, 0)

# 进行一次按键
def pressOneButton(keyNum):
    keyDown(keyNum)
    time.sleep(1)
    keyUP(keyNum)

# 两键同时按下例如CTRL + A
def pressTwoButton(firstKeyNum,secondKeyNum):
    keyDown(firstKeyNum)
    keyDown(secondKeyNum)
    time.sleep(0.1)
    keyUP(secondKeyNum)
    keyUP(firstKeyNum)

# 选定输入框覆盖原来的内容并覆盖然后回车，locate_str为经度纬度例如北京市区："116.389608,39.911172"
def inPutNowLocation(locate_str):
    # 模拟鼠标点击输入框
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    pressTwoButton(17, 65)  # 输入ctrl + A
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(CF_UNICODETEXT, locate_str)
    win32clipboard.CloseClipboard()
    pressTwoButton(17, 86)  # 输入ctrl + V
    pressOneButton(13)  # 输入回车

# 根据当前点和下一个点计算中间的路线
def oper(nowLocationPoint, nextLocationPoint):
    x1, y1 = nowLocationPoint.split(',')
    x2, y2 = nextLocationPoint.split(',')
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    tx = (x2 - x1) / 20
    ty = (y2 - y1) / 20
    for i in range(20):
        # 调整sleep时间以更改速度
        time.sleep(1 * speedIndex)
        # print("%f, %f" % (x1, y1))
        x1 = round(x1,6)
        y1 = round(y1,6)
        nowLocate = str(x1 + round((2 * random.random() - 1) / 10000,6)) + ',' + str(y1 + round((2 * random.random() - 1) / 10000,6))
        print(nowLocate)
        inPutNowLocation(nowLocate)
        x1 += tx
        y1 += ty

# 主函数，不断进行循环
def main():
    len = locationList.__len__()
    print(len)
    i = 0
    while(True):
        time.sleep(1)
        if i < len - 1:
            oper(locationList[i], locationList[i + 1])
            # print("%d, %d" % (i, i+1))
            i += 1
        else:
            oper(locationList[i], locationList[0])
            # print("%d, 0"%(i))
            i -= len - 1

if __name__ == "__main__":
    print("跑步10秒后即将开始....")
    time.sleep(10)
    print('跑步开始')
    main()

