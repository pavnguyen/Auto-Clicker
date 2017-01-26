# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import getpass
import os
import random
import sys
import time
import win32gui
from json import load
from subprocess import check_output
from time import sleep

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import pafy
import pyautogui
import win32con
from colorama import init, Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import rasdial
from list_timezone import LIST_TIME_ZONE
from config import SCREEN_RESOLUTION  # config.py
from screen_resolution import ScreenRes
import subprocess

init()


def get_tinyurl_clip(channel):
    load_result = False
    while load_result is False:
        try:
            links_tinyurl = tuple(open('ressources\LinksShorter\\' + str(channel) + '.txt', 'r'))
            random_int = random.randint(0, len(links_tinyurl) - 1)
            if 'http' in links_tinyurl[random_int].strip():
                yt_tinyurl = links_tinyurl[random_int].strip()
                load_result = True
        except:
            pass
    return yt_tinyurl


def get_random_vpn(name):
    value = random.randint(1, len(name))
    server = name.get(value)
    return server


def check_ping_is_ok():
    print('Check PING...')
    hostname = 'bing.com'
    try:
        response = os.system("ping -n 1 " + hostname)
        if response == 0:
            return True
    except:
        connect_purevpn()
        # connect_openvpn()


def check_country_is_ok():
    link = 'http://freegeoip.net/json/'
    try:
        country_name = load(urlopen(link))['country_name']
    except:
        return False
    if 'Vietnam' in country_name:
        return False
    else:
        return True


def connect_purevpn():
    if PUREVPN == 1:
        load_result = False
        rasdial.disconnect()
        print('Current VPN: ' + str(rasdial.get_current_vpn()))
        while load_result is False:
            rasdial.disconnect()
            sleep(1)

            # server = get_random_vpn(PURE_VPN_NAME)
            # user = 'purevpn0s1122211'
            # password = 'vunguyen'

            # server = get_random_vpn(PIA_VPN_NAME)
            # user = 'x3569491'
            # password = 'rUTPQnvnv7'

            server = 'HMA'
            user = 'avestergrd'
            password = 'vESsRzDB'

            rasdial.connect(server, user, password)  # connect to a vpn
            sleep(1)
            if check_ping_is_ok() is True:
                if check_country_is_ok() is True:
                    if set_zone() is True:
                        load_result = True


def connect_openvpn():
    if OPENVPN == 1:
        if NUMBER_MACHINE > TOTAL_CHANNEL or ADS_BOTTOM == 0 or PUREVPN == 0:
            load_result = False
            while load_result is False:
                try:
                    print('Try to Disconnect OpenVPN')
                    rasdial.disconnect()  # Disconnect PureVPN first
                    check_output("taskkill /im openvpn.exe /F", shell=True)
                except:
                    pass

                check_output('ipconfig /release', shell=True)
                check_output('ipconfig /renew', shell=True)

                print('Connect OpenVPN')
                cmd = '"C:\Program Files\OpenVPN\\bin\openvpn.exe"'
                value = random.randint(0, len(CONFIG_IP) - 1)
                print('Random Server: ' + CONFIG_IP[value].strip())
                if 'privateinternetaccess' in CONFIG_IP[value].strip():
                    parameters = ' --client --dev tun --proto udp --remote ' + CONFIG_IP[value].strip() + \
                                 ' --port 1198 --resolv-retry infinite --nobind --persist-key --persist-tun' \
                                 ' --cipher aes-128-cbc --auth sha1 --tls-client --remote-cert-tls server' \
                                 ' --auth-user-pass data\\auth.txt --comp-lzo --verb 1 --reneg-sec 0' \
                                 ' --crl-verify data\crl.rsa.2048.pem' \
                                 ' --auth-nocache' \
                                 ' --ca data\ca.rsa.2048.crt'
                else:
                    parameters = ' --tls-client --client --dev tun' \
                                 ' --remote ' + CONFIG_IP[value].strip() + \
                                 ' --proto udp --port 1197' \
                                 ' --lport 53 --persist-key --persist-tun --ca data\ca.crt --comp-lzo --mute 3' \
                                 ' --auth-user-pass data\\auth.txt' \
                                 ' --reneg-sec 0 --route-method exe --route-delay 2' \
                                 ' --verb 3 --log c:\\log.txt --status c:\\stat.db 1 --auth-nocache' \
                                 ' --crl-verify data\crl.pem --remote-cert-tls server' \
                                 ' --cipher aes-256-cbc --auth sha256'

                cmd += parameters
                try:
                    subprocess.Popen(cmd)
                    print('Please wait to connect to OpenVPN...')
                    countdown(8)
                except:
                    pass

                if check_ping_is_ok() is True:
                    if check_country_is_ok() is True:
                        if set_zone() is True:
                            load_result = True


def get_random_resolution():
    value = random.randint(1, len(SCREEN_RESOLUTION))
    width = SCREEN_RESOLUTION.get(value)[0]
    height = SCREEN_RESOLUTION.get(value)[1]
    return width, height


def get_recalcul_xy(x, y):
    x_new = x * X_SCREEN_SET / X_SCREEN
    y_new = y * Y_SCREEN_SET / Y_SCREEN

    return x_new, y_new


def get_info_length_youtube(url_real_youtube):
    video = pafy.new(url_real_youtube)
    return video.length


def set_screen_resolution():
    print('Primary screen resolution: {}x{}'.format(
        *ScreenRes.get()
    ))

    width, height = get_random_resolution()

    ScreenRes.set(width, height)
    # ScreenRes.set() # Set defaults
    try:
        windowList = []
        win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd), hwnd)),
                             windowList)
        cmdWindow = [i for i in windowList if 'auto viewer' in i[0].lower() or 'openvpn' in i[0].lower()
                     or 'auto_' in i[0].lower()]

        win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 0, 0, 320, 915, 0)
        # win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 1395, 0, 320, 915, 0)
    except:
        pass


def switch_main_window():
    try:
        BROWSER.switch_to.window(MAIN_WINDOW)
    except:
        print('Error: Browser can not take main window => Re-take main window ')
        BROWSER.switch_to.window(MAIN_WINDOW)
        pass


def switch_tab():
    # Switch tab to the new tab, which we will assume is the next one on the right
    try:
        BROWSER.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    except:
        try:
            print('Error: Switch tab to the new tab => Re-witch Tab')
            BROWSER.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        except:
            pass
        pass


def random_sleep():
    r = random.randint(4, 7)
    sleep(r)


def random_small_sleep():
    r = random.randint(1, 2)
    sleep(r)


def random_mouse_move():
    for i in range(random.randrange(3, 5)):
        try:
            print('Mouse Move')
            x = random.randint(5, 1024)
            y = random.randint(8, 768)
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            pyautogui.moveRel(x, y, random.random(), pyautogui.easeOutQuad)
            random_small_sleep()
        except:
            pass


def random_mouse_scroll():
    for i in range(random.randrange(2, 4)):
        try:
            print('Mouse Scroll')
            r = random.randint(-5000, 5000)
            pyautogui.scroll(r)
            random_small_sleep()
            r = random.randint(-5000, 5000)
            pyautogui.scroll(-r)
            random_small_sleep()
        except:
            pass
    try:
        r = random.randint(-5000, 5000)
        pyautogui.scroll(r)
        random_small_sleep()
    except:
        pass


def get_path_profile_firefox():
    # Firefox Parameters
    user_name = getpass.getuser()
    path_profil = 'C:/Users/' + user_name + '/AppData/Roaming/Mozilla/Firefox/Profiles/'
    profil_name = os.listdir(path_profil)[0]
    path_profil += profil_name
    return path_profil


def get_position_mouse():
    try:
        x, y = pyautogui.position()
        positionStr = '    X: ' + str(x).rjust(4) + '  Y: ' + str(y).rjust(4)
        print(positionStr)
    except:
        pass


def set_zone():
    try:
        link = 'http://freegeoip.net/json/'
        latitude = load(urlopen(link))['latitude']
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Latitude] => ' + str(latitude) + Style.RESET_ALL)
        longitude = load(urlopen(link))['longitude']
        print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Longitude] => ' + str(longitude) + Style.RESET_ALL)
        timestamp = str(time.time())

        # Public IP & DateTime
        ip = urlopen('http://ip.42.pl/raw').read()
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[IP] => ' + ip + Style.RESET_ALL)

        region_name = load(urlopen(link))['region_name']
        print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Region] => ' + region_name + Style.RESET_ALL)

        city = load(urlopen(link))['city']
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[City] => ' + city + Style.RESET_ALL)

        time_zone = load(urlopen(link))['time_zone']
        print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Time Zone] => ' + time_zone + Style.RESET_ALL)

        # Google API service form Vu.nomos
        link = 'https://maps.googleapis.com/maps/api/timezone/json?location=' + str(latitude) + ',' + \
               str(longitude) + '&timestamp=' + timestamp + '&key=AIzaSyAC2ESW2jOFDdABT6hZ4AKfL7U8jQRSOKA'
        timeZoneId = load(urlopen(link))['timeZoneId']

        zone_to_set = LIST_TIME_ZONE.get(timeZoneId)
        print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + 'Synchronize ' + zone_to_set + Style.RESET_ALL)
        if zone_to_set.strip() != '':
            check_output("tzutil /s " + '"' + zone_to_set + '" ', shell=True)
            return True
    except:
        return False
        pass


def countdown(timing):
    while timing:
        mins, secs = divmod(timing, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        timing -= 1
        print(Fore.LIGHTCYAN_EX + Back.BLACK + 'Please wait...' + timeformat + Style.RESET_ALL, end='\r')


def get_params(param):
    return CONFIG_JSON['DEFAULT'][0][param]


def main():
    global BROWSER
    global MAIN_WINDOW
    global ADS_BOTTOM
    global ADS_RIGHT
    global CLOSE_ADS_BOTTOM
    global TOTAL_CHANNEL
    global PUREVPN
    global OPENVPN
    global X_SCREEN_SET
    global Y_SCREEN_SET
    global NUMBER_MACHINE
    global X_SCREEN
    global Y_SCREEN
    global KEYWORDS
    global CONFIG_IP
    global CONFIG_JSON
    global USER_CONFIG
    global COUNTER_TOURS
    global TOTAL_CLICKS_ADS_BOTTOM
    global FILE_URL

    with open('config_auto_clicker.json') as data_file:
        CONFIG_JSON = load(data_file)

    USER_CONFIG = get_params('USER_CONFIG')
    ADS_BOTTOM = int(get_params('ADS_BOTTOM'))
    ADS_RIGHT = int(get_params('ADS_RIGHT'))
    CLOSE_ADS_BOTTOM = int(get_params('CLOSE_ADS_BOTTOM'))
    TOTAL_CHANNEL = int(get_params('TOTAL_CHANNEL'))
    BOUCLE_SUPER_VIP = int(get_params('BOUCLE_SUPER_VIP'))
    PUREVPN = int(get_params('PureVPN'))
    OPENVPN = int(get_params('OpenVPN'))
    X_SCREEN = int(get_params('WIDTH'))
    Y_SCREEN = int(get_params('HEIGHT'))
    X_SCREEN_SET, Y_SCREEN_SET = pyautogui.size()
    CONFIG_IP = tuple(open('ressources\config_ip.txt', 'r'))
    KEYWORDS = tuple(open('ressources\keyword.txt', 'r'))

    ADS_BOTTOM = 0

    # Resize Screen and set Always on TOP
    set_screen_resolution()

    print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'Auto Blog [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

    if len(sys.argv) > 1:
        NUMBER_MACHINE = int(sys.argv[1])
        # FILE_URL = sys.argv[2]
    else:
        print(Back.BLACK + Fore.LIGHTWHITE_EX + ' ' * 3 + '[ Please enter the Machine Number: ]' +
              Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX)
        print(Style.RESET_ALL)

        NUMBER_MACHINE = str(raw_input())

    # Firefox Parameters
    path_profil = get_path_profile_firefox()
    binary_ff = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

    # modulo = random.randint(2, 3)

    for z in range(200):
        # connect_openvpn()
        connect_purevpn()
        start_time = time.time()
        # Open Firefox with default profile
        fp = webdriver.FirefoxProfile(path_profil)
        BROWSER = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary_ff)
        BROWSER.maximize_window()

        try:
            MAIN_WINDOW = BROWSER.current_window_handle
        except:
            MAIN_WINDOW = BROWSER.current_window_handle
            pass

        # View before detect and click real ads
        timing_view = random.randint(10, 20)

        for j in range(50):
            y = random.randint(13, 17)
            try:
                url_view = get_tinyurl_clip(y)
                print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'URL VIEW: ' + str(y) + ' >> ' +
                      Style.RESET_ALL + Back.BLACK + Fore.LIGHTWHITE_EX + url_view + '' + Style.RESET_ALL)
                BROWSER.get(url_view)
                countdown(10)

                # Click Skip ads
                try:
                    print('Click Skip Ads!')
                    pyautogui.moveTo(1540, 135, random.random(), pyautogui.easeOutQuad)
                    pyautogui.click(1540, 135)
                except:
                    pyautogui.click(1540, 133)
                    continue
            except:
                continue
            countdown(timing_view)

        random_mouse_move()
        COUNTER_TOURS += 1

        print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + ' ' * 9 + 'FINISH -> Tours -> ' +
              Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + str(COUNTER_TOURS) + '' +
              Style.RESET_ALL)
        print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)

        print(Fore.LIGHTGREEN_EX + Back.BLACK + '\n[Total timing]' + Style.RESET_ALL + ' ' +
              str(datetime.timedelta(seconds=time.time() - start_time)) + '')
        print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)

        print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
        print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'Auto Blog[AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

        try:
            BROWSER.delete_all_cookies()
            BROWSER.quit()
        except:
            pass
    try:
        BROWSER.delete_all_cookies()
        BROWSER.quit()
    except:
        pass

    raw_input()


########################################################################################################################
#                                                Main Program                                                          #
# Arguments:                                                                                                           #
# argv[1]: NUMBER_MACHINE                                                                                              #
#                                                                                                                      #
########################################################################################################################


if __name__ == "__main__":
    COUNTER_TOURS = 0
    TOTAL_CLICKS_ADS_BOTTOM = 0

    main()
