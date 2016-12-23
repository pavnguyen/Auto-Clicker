# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import getpass
import os
import random
import sys
import time
from json import load
from subprocess import check_output
from time import sleep

import win32gui

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import pafy
import pyautogui
import selenium.webdriver.support.ui as ui
import win32con
from colorama import init, Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import rasdial
from list_timezone import LIST_TIME_ZONE
from config import PARAMS
from config import SCREEN_RESOLUTION  # config.py
from config import USER_PASS
from config import VPN_NAME
from screen_resolution import ScreenRes
import subprocess

init()


def get_tinyurl_clip(channel):
    load = False
    while load is False:
        try:
            links_tinyurl = tuple(open('ressources\LinksTinyURL\\' + str(channel) + '.txt', 'r'))
            random_int = random.randint(0, len(links_tinyurl))
            if 'http' in links_tinyurl[random_int].strip():
                result = links_tinyurl[random_int].strip()
            load = True
        except:
            pass
    return result


def get_random_vpn():
    value = random.randint(1, len(VPN_NAME))
    server = VPN_NAME.get(value)
    return server


def connect_pure_vpn():
    if PARAMS.get('PureVPN') == 1 and 'ADS_BOTTOM' == 1 and NUMBER_MACHINE <= TOTAL_CHANNEL:
        rasdial.disconnect()
        print('Current VPN: ' + str(rasdial.get_current_vpn()))
        while rasdial.is_connected() is False:
            rasdial.disconnect()
            sleep(1)
            server = get_random_vpn()
            # value = random.randint(1, 2)

            if NUMBER_MACHINE <= 6:
                value = 1
            elif 6 < NUMBER_MACHINE <= TOTAL_CHANNEL:
                value = 2
            user = USER_PASS.get(value)[0]
            password = USER_PASS.get(value)[1]
            rasdial.connect(server, user, password)  # connect to a vpn
            sleep(1)
            print('Current VPN: ' + str(rasdial.get_current_vpn()))


def connect_openvpn():
    global PROCESS_VPN
    if (PARAMS.get('OpenVPN') == 1 and NUMBER_MACHINE > TOTAL_CHANNEL) or ADS_BOTTOM == 0:
        print('Connect OpenVPN')
        cmd = '"C:\Program Files\OpenVPN\\bin\openvpn.exe"'
        value = random.randint(0, len(CONFIG_IP))
        print('Random IP: ' + CONFIG_IP[value].strip())
        parameters = ' --tls-client --client --dev tun ' \
                     '--remote ' + CONFIG_IP[value].strip() + \
                     ' --proto udp --port 1197 ' \
                     '--lport 53 --persist-key ' \
                     '--persist-tun ' \
                     '--ca data\ca.crt ' \
                     '--comp-lzo --mute 3 ' \
                     '--tun-mtu 1400 --mssfix 1360 ' \
                     '--auth-user-pass data\\auth.txt ' \
                     '--reneg-sec 0 --keepalive 10 120 ' \
                     '--route-method exe --route-delay 2 ' \
                     '--verb 3 --log c:\\log.txt ' \
                     '--status c:\\stat.db 1 ' \
                     '--auth-nocache ' \
                     '--crl-verify data\crl.pem ' \
                     '--remote-cert-tls server ' \
                     '--block-outside-dns ' \
                     '--cipher aes-256-cbc ' \
                     '--auth sha256'
        cmd += parameters
        PROCESS_OPENVPN = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print('Please wait to connect to OpenVPN...')
        countdown(10)
        return PROCESS_OPENVPN


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
        cmdWindow = [i for i in windowList if "auto clicker" in i[0].lower()]

        # win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 1050, 0, 670, 160, 0)
        win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 1395, 0, 320, 915, 0)
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


def search_google():
    load = False
    counter = 0
    while load is False and counter < 3:
        counter += 1
        try:
            key_search = get_key_search()
            sleep(1)
            BROWSER.get('https://encrypted.google.com/#q=' + key_search)
            countdown(3)
            try:
                first_result = ui.WebDriverWait(BROWSER, 15).until(lambda BROWSER:
                                                                   BROWSER.find_element_by_class_name('rc'))
                first_link = first_result.find_element_by_tag_name('a')
                # Open the link in a new tab by sending key strokes on the element
                # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
                first_link.send_keys(Keys.CONTROL + Keys.RETURN)
                load = True
            except:
                print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"rc\" => Load \"ads-ad\" ' +
                      Style.RESET_ALL)
                try:
                    first_result = ui.WebDriverWait(BROWSER, 3).until(lambda BROWSER:
                                                                      BROWSER.find_element_by_class_name('ads-ad'))
                    first_link = first_result.find_element_by_tag_name('a')
                    first_link.send_keys(Keys.CONTROL + Keys.RETURN)
                    load = True
                except:
                    print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"ads-ad\" => Reload... ' +
                          Style.RESET_ALL)
                    pass
            pass
        except:
            pass
    # Switch tab to the new tab, which we will assume is the next one on the right
    switch_tab()
    random_small_sleep()
    # Take hand the window opener
    switch_main_window()
    return load


def detect_and_click_ads_bottom(url, timing_ads):
    load = False
    try:
        BROWSER.get(url)
        countdown(3)
        try:
            first_result = ui.WebDriverWait(BROWSER, timing_ads).until(lambda BROWSER:
                                                                       BROWSER.find_element_by_class_name('adDisplay'))
            first_link = first_result.find_element_by_tag_name('a')
            first_link.send_keys(Keys.CONTROL + Keys.RETURN)

            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Class \"adDisplay\" => ' + Style.RESET_ALL +
                  Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)
            load = True
        except:
            try:
                first_result = ui.WebDriverWait(BROWSER, 3).until \
                    (lambda BROWSER: BROWSER.find_element_by_class_name('adDisplay'))
                first_link = first_result.find_element_by_tag_name('a')
                first_link.send_keys(Keys.CONTROL + Keys.RETURN)

                print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Class \"adDisplay\" => ' + Style.RESET_ALL +
                      Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)

                load = True

                print(Fore.LIGHTRED_EX + 'Error: adDisplay => Load \"AdSense\"' + Style.RESET_ALL)
            except:
                try:
                    first_result = ui.WebDriverWait(BROWSER, 3).until(lambda BROWSER:
                                                                      BROWSER.find_element_by_id('AdSense'))
                    first_link = first_result.find_element_by_tag_name('a')
                    first_link.send_keys(Keys.CONTROL + Keys.RETURN)

                    print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Id \"AdSense\" => ' + Style.RESET_ALL +
                          Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)
                    load = True
                except:
                    print(Fore.LIGHTRED_EX + 'Error: AdSense => Reload clip!!!' + Style.RESET_ALL)
                    pass
                pass
    except:
        pass
    # Switch tab to the new tab, which we will assume is the next one on the right
    switch_tab()
    random_sleep()
    random_mouse_scroll()
    random_mouse_move()
    return load


def click_ads_right():
    if ADS_RIGHT == 1:
        try:
            x, y = get_recalcul_xy(1330, 270)
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            pyautogui.keyDown('ctrl')
            pyautogui.click()
            pyautogui.keyUp('ctrl')
            sleep(1)
            x, y = get_recalcul_xy(1335, 423)
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            pyautogui.keyDown('ctrl')
            pyautogui.click()
            pyautogui.keyUp('ctrl')
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT)
            print('>> Ads Right >> Try to Click Ads RIGHT')
            print(Style.RESET_ALL)
        except:
            pass


def replay_clip():
    try:
        print('-> Mouse move to Clip')
        x, y = get_recalcul_xy(540, 450)
        pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
        get_position_mouse()
        sleep(0.25)
        pyautogui.click(x, y)
        print('-> Mouse click to REPLAY')
        random_mouse_move()
    except:
        pass


def random_sleep():
    r = random.randint(4, 8)
    sleep(r)


def random_small_sleep():
    r = random.randint(1, 3)
    sleep(r)


def random_mouse_move():
    for i in range(random.randrange(0, 5)):
        x = random.randint(5, 1024)
        y = random.randint(8, 768)
        pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
        pyautogui.moveRel(x, y, random.random(), pyautogui.easeOutQuad)
        random_small_sleep()


def random_mouse_scroll():
    for i in range(random.randrange(0, 2)):
        r = random.randint(-5000, 5000)
        pyautogui.scroll(r)
        random_small_sleep()
        r = random.randint(-5000, 5000)
        pyautogui.scroll(-r)
        random_small_sleep()
    r = random.randint(-5000, 5000)
    pyautogui.scroll(r)


def get_path_profile_firefox():
    # Firefox Parameters
    user_name = getpass.getuser()
    path_profil = 'C:/Users/' + user_name + '/AppData/Roaming/Mozilla/Firefox/Profiles/'
    profil_name = os.listdir(path_profil)[0]
    path_profil += profil_name
    return path_profil


def get_position_mouse():
    x, y = pyautogui.position()
    positionStr = '    X: ' + str(x).rjust(4) + '  Y: ' + str(y).rjust(4)
    print(positionStr)


def get_key_search():
    random_int = random.randint(1, 5500)
    print(Fore.LIGHTYELLOW_EX + Back.BLACK + 'Keywords >> ' + Style.RESET_ALL + Fore.LIGHTGREEN_EX +
          Back.BLACK + KEYWORDS[random_int].strip() + Style.RESET_ALL)
    return KEYWORDS[random_int].strip('')


def set_zone():
    try:
        print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + time.ctime() + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Synchronize Time Zone ...' + Style.RESET_ALL)

        link = 'http://freegeoip.net/json/'
        latitude = load(urlopen(link))['latitude']
        longitude = load(urlopen(link))['longitude']
        timestamp = str(time.time())

        # Public IP & DateTime
        ip = urlopen('http://ip.42.pl/raw').read()
        region_name = load(urlopen('http://freegeoip.net/json/'))['region_name']
        city = load(urlopen('http://freegeoip.net/json/'))['city']
        time_zone = load(urlopen('http://freegeoip.net/json/'))['time_zone']

        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[IP] => ' + ip + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Region] => ' + region_name + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[City] => ' + city + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Time Zone] => ' + time_zone + Style.RESET_ALL)

        # Google API service form Vu.nomos
        link = 'https://maps.googleapis.com/maps/api/timezone/json?location=' + str(latitude) + ',' + \
               str(longitude) + '&timestamp=' + timestamp + '&key=AIzaSyAC2ESW2jOFDdABT6hZ4AKfL7U8jQRSOKA'
        timeZoneId = load(urlopen(link))['timeZoneId']
        zone_to_set = LIST_TIME_ZONE.get(timeZoneId)
        check_output("tzutil /s " + '"' + zone_to_set + '" ', shell=True)
    except:
        pass


def countdown(timing):
    while timing:
        mins, secs = divmod(timing, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        timing -= 1
        print(Fore.LIGHTCYAN_EX + Back.BLACK + Style.BRIGHT + 'Please wait...' + timeformat + Style.RESET_ALL, end='\r')


########################################################################################################################
#                                                Main Program                                                          #
# Arguments:                                                                                                           #
# argv[1]: NUMBER_MACHINE                                                                                              #
#                                                                                                                      #
########################################################################################################################
global BROWSER
global MAIN_WINDOW
global ADS_BOTTOM
global ADS_RIGHT
global TOTAL_CHANNEL
global X_SCREEN_SET
global Y_SCREEN_SET
global NUMBER_MACHINE
global X_SCREEN
global Y_SCREEN
global KEYWORDS
global CONFIG_IP
global COUNTER_TOURS
global TOTAL_CLICKS_ADS_BOTTOM

ADS_BOTTOM = PARAMS.get('ADS_BOTTOM')
ADS_RIGHT = PARAMS.get('ADS_RIGHT')
TOTAL_CHANNEL = PARAMS.get('TOTAL_CHANNEL')
BOUCLE_SUPER_VIP = PARAMS.get('BOUCLE_SUPER_VIP')
X_SCREEN = PARAMS.get('WIDTH')
Y_SCREEN = PARAMS.get('HEIGHT')
X_SCREEN_SET, Y_SCREEN_SET = pyautogui.size()
CONFIG_IP = tuple(open('ressources\config_ip.txt', 'r'))
KEYWORDS = tuple(open('ressources\keyword.txt', 'r'))
COUNTER_TOURS = 0
TOTAL_CLICKS_ADS_BOTTOM = 0

# Resize Screen and set Always on TOP
set_screen_resolution()

print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'Auto Clicker [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

if len(sys.argv) > 1:
    NUMBER_MACHINE = int(sys.argv[1])
else:
    print(Back.BLACK + Fore.LIGHTWHITE_EX + ' ' * 3 + '[ Please enter the Machine Number: ]' +
          Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX)
    print(Style.RESET_ALL)

    NUMBER_MACHINE = str(raw_input())

print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + "Number Machine: " + str(NUMBER_MACHINE) + '' + Style.RESET_ALL)
print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + "Total Channel: " +
      str(TOTAL_CHANNEL) + '' + Style.RESET_ALL)

# Firefox Parameters
path_profil = get_path_profile_firefox()
binary_ff = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

for z in range(BOUCLE_SUPER_VIP):
    try:
        sleep(0.5)
        check_output("taskkill /im openvpn.exe /F", shell=True)
        countdown(3)
    except:
        pass
    connect_pure_vpn()  # PureVPN
    PROCESS_OPENVPN = connect_openvpn()  # OpenVPN
    set_zone()

    for i in range(NUMBER_MACHINE, TOTAL_CHANNEL + NUMBER_MACHINE):
        if ADS_BOTTOM == 1:
            print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' + Style.RESET_ALL
                  + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL + '')

        start_time = time.time()

        # Open Firefox with default profile
        if i == NUMBER_MACHINE or ADS_BOTTOM == 1:
            fp = webdriver.FirefoxProfile(path_profil)
            BROWSER = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary_ff)
            BROWSER.maximize_window()

        # Check Whoer once!!!
        if i == NUMBER_MACHINE:
            print(Back.BLACK + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Please wait to check Whoer.net... '
                  + Style.RESET_ALL)
            load = False
            while load is False:
                try:
                    print('Check Whoer...')
                    BROWSER.get('https://whoer.net/')
                    countdown(3)
                    ui.WebDriverWait(BROWSER, 10).until(lambda BROWSER: BROWSER.find_element_by_id('anonym_level'))
                    id_level = BROWSER.find_element_by_id('anonym_level').text
                    load = True
                except:
                    pass
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Status] => ' + Style.RESET_ALL +
                  Back.BLACK + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + id_level + '' + Style.RESET_ALL)

            BROWSER.delete_all_cookies()

        # Save the window opener
        try:
            MAIN_WINDOW = BROWSER.current_window_handle
        except:
            MAIN_WINDOW = BROWSER.current_window_handle
            pass

        #################
        # Google Search #
        #################
        if ADS_BOTTOM == 1:
            try:
                total_key = random.randint(1, 3)
                for j in range(total_key):
                    loaded_google = search_google()  # Search Google with keywords

                    print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Search Key] => ' + Style.RESET_ALL +
                          Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[ OK ]' + Style.RESET_ALL)
                    random_small_sleep()
            except:
                print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Search Key] => ' + Style.RESET_ALL +
                      Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + 'FAILED!!!' + Style.RESET_ALL)
                pass

        #####################
        # Detect Ads Bottom #
        #####################
        switch_main_window()

        print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' + Style.RESET_ALL
              + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL + '')

        file_channel = i

        if i <= TOTAL_CHANNEL:
            file_channel = i
        else:
            file_channel = (i + TOTAL_CHANNEL) % TOTAL_CHANNEL

        if file_channel == 0:
            file_channel = TOTAL_CHANNEL

        url = get_tinyurl_clip(str(file_channel))

        print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'URL >> ' + Style.RESET_ALL +
              Back.BLACK + Fore.LIGHTWHITE_EX + url + '' + Style.RESET_ALL)

        # Check Ads Bottom
        found_ads_bottom = False
        if ADS_BOTTOM == 1:
            counter = 0
            timing_ads = random.randint(25, 39)
            while found_ads_bottom is False and counter < 3:
                try:
                    counter += 1
                    print("Test Ads Bottom: " + str(counter))
                    found_ads_bottom = detect_and_click_ads_bottom(url, timing_ads)
                    if found_ads_bottom is True:
                        TOTAL_CLICKS_ADS_BOTTOM += 1
                        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Ads Bottom] => ' +
                              Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT +
                              '[FOUND & CLICKED]' + Style.RESET_ALL)
                        print(
                            Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' +
                            Style.RESET_ALL + Fore.LIGHTGREEN_EX + Back.BLACK +
                            str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL)
                except:
                    try:
                        BROWSER.quit()
                    except:
                        pass
                    continue

            if found_ads_bottom is False:
                try:
                    BROWSER.quit()
                except:
                    pass
                continue
        else:
            print(Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + '-----------[MODE] VIEW ONLY----------' +
                  Style.RESET_ALL)
            try:
                BROWSER.get(url)
                countdown(2)
            except:
                pass

        COUNTER_TOURS += 1

        #####################
        # Back to the video #
        #####################

        switch_main_window()

        try:
            sleep(1)
            current_url = BROWSER.current_url
            print('Current url:' + current_url)
        except:
            print('Current Url is not found!')
            pass

        if current_url is not None:
            try:
                wait_time = get_info_length_youtube(current_url) - random.randint(40, 60)
                if wait_time < 0 or wait_time > 240:
                    wait_time = random.randint(150, 180)
            except:
                wait_time = random.randint(150, 180)

        if found_ads_bottom is True:
            replay_clip()  # Click and replay clip

            # Try to close Ads
            random_close = random.randint(0, 1)
            if random_close == 0:
                try:
                    x, y = get_recalcul_xy(845, 551)
                    print('Try to close Ads: X->' + str(x) + ' Y->' + str(y))
                    pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
                    sleep(0.25)
                    pyautogui.click(x, y)
                except:
                    pass

        random_mouse_move()
        ###################
        # Click Ads RIGHT #
        ###################

        click_ads_right()

        if ADS_BOTTOM == 1:
            print(Fore.LIGHTYELLOW_EX + Back.BLACK + '[Search key] => ' + Style.RESET_ALL
                  + Fore.LIGHTGREEN_EX + Back.BLACK + str(total_key) + Style.RESET_ALL)
            print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + '[Duration to click ads]' + Style.RESET_ALL +
                  Back.BLACK + Fore.LIGHTWHITE_EX + ' ' +
                  str(datetime.timedelta(seconds=time.time() - start_time)) + '' + Style.RESET_ALL)
            print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' + Style.RESET_ALL
                  + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL)

        print(Fore.LIGHTMAGENTA_EX + '_' * 37 + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + ' ' * 8 + 'FINISH -> Tours -> ' +
              Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + str(COUNTER_TOURS) + '' +
              Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + '-' * 37 + Style.RESET_ALL)

        if found_ads_bottom is True or ADS_BOTTOM == 0:
            countdown(wait_time)  # Wait n minutes to view

        print(Fore.LIGHTGREEN_EX + Back.BLACK + '\n[Total timing]' + Style.RESET_ALL + ' ' +
              str(datetime.timedelta(seconds=time.time() - start_time)) + '')
        print(Fore.LIGHTMAGENTA_EX + '_' * 37 + Style.RESET_ALL)

        print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
        print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'Auto Clicker [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

        if ADS_BOTTOM == 1:
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

if ADS_BOTTOM == 1:
    print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' + Style.RESET_ALL
          + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL + '')
    print(Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + 'Press ENTER to close...' + '')
raw_input()
