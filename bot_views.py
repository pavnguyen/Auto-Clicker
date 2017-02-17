import time
import webbrowser
from subprocess import check_output

url = str(raw_input("Enter YouTube URL : "))
refresh = raw_input("Enter refresh rate(seconds) : ")
brow = raw_input("Enter your default browser : ")


def OpenUrl():
    print("Successfully Viewd. ")
    # os.system("TASKKILL /F /IM " + brow + ".exe")
    try:
        check_output("taskkill /F /IM " + brow + ".exe", shell=True)
    except:
        pass

    webbrowser.open(str(url))
    time.sleep(int(refresh))


for i in range(3):
    OpenUrl()
