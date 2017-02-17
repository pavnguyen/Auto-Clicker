import os
import sys
import time
import webbrowser
from subprocess import check_output

refresh = raw_input("Enter refresh rate(seconds) : ")
brow = raw_input("Enter your default browser : ")


def openUrl(url):
    print("Successfully Viewed. ")
    try:
        if sys.platform == 'win32':
            check_output("taskkill /F /IM " + brow + ".exe", shell=True)
        else:
            os.system(" killall -9 " + brow)
    except:
        pass

    webbrowser.open(str(url))
    time.sleep(int(refresh))


urls = tuple(open('ressources/Links_bot_views.txt', 'r'))

for i in range(0, len(urls) - 1):
    for j in range(100):
        OpenUrl(urls[i])
