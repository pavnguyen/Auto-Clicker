# -*- coding: utf-8 -*-
from __future__ import print_function

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

import pyautogui
import selenium.webdriver.support.ui as ui
import win32con
from colorama import init, Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import rasdial
from list_timezone import LIST_TIME_ZONE
from config import SCREEN_RESOLUTION  # config.py
from config import PURE_VPN_NAME
from screen_resolution import ScreenRes
import subprocess
import getpass
import shutil, errno
import smtplib

init()


def send_email_alert():
    try:
        fromaddr = 'vu.nomos@gmail.com'
        toaddrs = 'vunguyen.xbt@gmail.com'
        msg = 'Probleme d\'Autoclicker'
        username = 'vu.nomos@gmail.com'
        password = 'Params$&#!'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.close()
    except:
        pass


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
        if PURE_VPN_NAME == 0:
            connect_openvpn()
        else:
            connect_purevpn()


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


def connect_openvpn():
    if OPENVPN == 1 or ADS_BOTTOM == 0:
        load_result = False
        counter_connect = 0
        while load_result is False:
            if counter_connect >= 3:
                send_email_alert()
            counter_connect += 1
            if sys.platform == 'win32':
                try:
                    print('Try to Disconnect OpenVPN')
                    rasdial.disconnect()  # Disconnect params_PureVPN first
                    check_output("taskkill /im openvpn.exe /F", shell=True)
                except:
                    pass

                check_output('ipconfig /release', shell=True)
                check_output('ipconfig /renew', shell=True)

            print('Connect OpenVPN')
            if sys.platform == 'win32':
                cmd = '"C:/Program Files/OpenVPN/bin/openvpn.exe"'
            else:
                cmd = '/etc/openvpn/openvpn'
            value = random.randint(0, len(CONFIG_IP) - 1)
            print('Random Server: ' + CONFIG_IP[value].strip())
            if 'privateinternetaccess' in CONFIG_IP[value].strip():
                parameters = ' --client --dev tun --proto udp --remote ' \
                             + CONFIG_IP[value].strip() + \
                             ' --port 1198 --resolv-retry infinite --nobind --persist-key --persist-tun' \
                             ' --cipher aes-128-cbc --auth sha1 --tls-client --remote-cert-tls server' \
                             ' --auth-user-pass ressources/params_PIA/data/auth.txt ' \
                             '--comp-lzo --verb 1 --reneg-sec 0' \
                             ' --crl-verify ressources/params_PIA/data/crl.rsa.2048.pem' \
                             ' --auth-nocache' \
                             ' --ca ressources/params_PIA/data/ca.rsa.2048.crt' \
                    # ' --block-outside-dns'
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
        cmdWindow = [i for i in windowList if 'auto clicker' in i[0].lower() or 'openvpn' in i[0].lower()]
        win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 1395, 0, 320, 915, 0)
    except:
        pass


def switch_main_window():
    try:
        BROWSER.switch_to.window(MAIN_WINDOW)
    except:
        print('Error: Browser can not take MAIN WINDOW')
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


def search_google():
    load_result = False
    counter = 0
    while load_result is False and counter < 2:
        counter += 1
        try:
            key_search = get_key_search()
            sleep(2)
            BROWSER.get('https://encrypted.google.com/#q=' + key_search)
            countdown(2)
            try:
                first_result = ui.WebDriverWait(BROWSER, 15).until(lambda BROWSER:
                                                                   BROWSER.find_element_by_class_name('rc'))
                first_link = first_result.find_element_by_tag_name('a')
                # Open the link in a new tab by sending key strokes on the element
                # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
                first_link.send_keys(Keys.CONTROL + Keys.RETURN)
                load_result = True
            except:
                print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"rc\" => Load \"ads-ad\" ' +
                      Style.RESET_ALL)
                try:
                    first_result = ui.WebDriverWait(BROWSER, 8).until(lambda BROWSER:
                                                                      BROWSER.find_element_by_class_name('ads-ad'))
                    first_link = first_result.find_element_by_tag_name('a')
                    first_link.send_keys(Keys.CONTROL + Keys.RETURN)
                    load_result = True
                except:
                    print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"ads-ad\" => Reload... ' +
                          Style.RESET_ALL)
                    switch_main_window()
                    pass
            pass
        except:
            pass

    # Switch tab to the new tab, which we will assume is the next one on the right
    switch_tab()
    random_small_sleep()
    # Take hand the window opener
    switch_main_window()
    return load_result


def random_sleep():
    r = random.randint(3, 5)
    sleep(r)


def random_small_sleep():
    r = random.randint(1, 2)
    sleep(r)


def random_mouse_move():
    print('Mouse Move')
    for i in range(random.randrange(2, 4)):
        try:
            x = random.randint(5, 1380)
            y = random.randint(110, 890)
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            pyautogui.moveRel(x, y, random.random(), pyautogui.easeOutQuad)
            random_small_sleep()
        except:
            pass


def random_mouse_scroll():
    print('Mouse Scroll')
    for i in range(random.randrange(2, 4)):
        try:
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


def get_key_search():
    random_int = random.randint(1, 5500)
    print(Fore.LIGHTYELLOW_EX + Back.BLACK + 'Keywords >> ' + Style.RESET_ALL + Fore.LIGHTGREEN_EX +
          Back.BLACK + KEYWORDS[random_int].strip() + Style.RESET_ALL)
    return KEYWORDS[random_int].strip('')


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
    while timing >= 0:
        mins, secs = divmod(timing, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        timing -= 1
        print(Fore.LIGHTCYAN_EX + Back.BLACK + 'Please wait...' + timeformat + Style.RESET_ALL, end='\r')


def get_params(param):
    return CONFIG_JSON['DEFAULT'][0][param]


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("parent.lock", "lock", ".parentlock"))
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            pass


def backup_profile(numberMachine):
    numberMachine = str(numberMachine)
    userName = getpass.getuser()
    path = 'C:/Users/' + userName + '/AppData/Local/Temp/'
    for tmp in os.listdir(path):
        if 'rust_mozprofile' in tmp:
            profilName = tmp
            path += profilName
            pass
    print(path)
    if not os.path.exists('ressources/Profils/' + numberMachine):
        copyanything(path, 'ressources/Profils/' + numberMachine)
    else:
        try:
            shutil.rmtree('ressources/Profils/' + numberMachine)
            copyanything(path, 'ressources/Profils/' + numberMachine)
        except:
            pass
    try:
        BROWSER.quit()
    except:
        pass

    try:
        shutil.rmtree(path)
    except:
        print('Cannot delete!!!')
        pass
    print('Profil Firefox is backup!!!')


def main(optional):
    global BROWSER
    global MAIN_WINDOW
    global PUREVPN
    global OPENVPN
    global X_SCREEN_SET
    global Y_SCREEN_SET
    global X_SCREEN
    global Y_SCREEN
    global KEYWORDS
    global CONFIG_IP
    global CONFIG_IP_PURE
    global CONFIG_JSON
    global GOOGLE_SEARCH

    with open('config_auto_clicker.json') as data_file:
        CONFIG_JSON = load(data_file)

    GOOGLE_SEARCH = int(get_params('GOOGLE_SEARCH'))
    PUREVPN = int(get_params('PureVPN'))
    OPENVPN = int(get_params('OpenVPN'))
    X_SCREEN = int(get_params('WIDTH'))
    Y_SCREEN = int(get_params('HEIGHT'))
    X_SCREEN_SET, Y_SCREEN_SET = pyautogui.size()
    CONFIG_IP = tuple(open('ressources/params_PIA/list_PIA.txt', 'r'))
    KEYWORDS = tuple(open('ressources/keyword.txt', 'r'))

    # Resize Screen and set Always on TOP
    set_screen_resolution()

    # Firefox Parameters
    if sys.platform == 'win32':
        path_profil = get_path_profile_firefox()
        binary_ff = FirefoxBinary(r'C:/Program Files (x86)/Mozilla Firefox/firefox.exe')

    for z in range(int(optional)):
        connect_openvpn()  # OpenVPN

        # Open Firefox with default profile
        if sys.platform == 'win32':
            fp = webdriver.FirefoxProfile(path_profil)
            BROWSER = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary_ff)
        else:
            BROWSER = webdriver.Firefox()
        BROWSER.maximize_window()

        # Save the window opener
        try:
            MAIN_WINDOW = BROWSER.current_window_handle
        except:
            pass

        try:
            total_key = random.randint(8, 9)
            for j in range(total_key):
                loaded_google = search_google()  # Search Google with keywords

                print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Search Key] => ' + Style.RESET_ALL +
                      Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[ OK ]' + Style.RESET_ALL)
                random_small_sleep()
                switch_main_window()
        except:
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Search Key] => ' + Style.RESET_ALL +
                  Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + 'FAILED!!!' + Style.RESET_ALL)
            pass

        countdown(200)
        backup_profile(z)

########################################################################################################################
#                                                Main Program                                                          #
# Arguments:                                                                                                           #
# argv[1]: NUMBER_MACHINE                                                                                              #
#                                                                                                                      #
########################################################################################################################


if __name__ == "__main__":
    main(100)
