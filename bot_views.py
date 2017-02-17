import time
import webbrowser
from subprocess import check_output

refresh = raw_input("Enter refresh rate(seconds) : ")
brow = raw_input("Enter your default browser : ")


def openUrl(url):
    print("Successfully Viewed. ")
    try:
        check_output("taskkill /F /IM firefox.exe", shell=True)
    except:
        pass

    webbrowser.open(str(url))
    time.sleep(int(refresh))


urls = tuple(open('ressources/Links_bot_views.txt', 'r'))

for i in range(0, len(urls) - 1):
    for j in range(100):
        OpenUrl(urls[i])
