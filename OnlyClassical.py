# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import getpass
import os
import random
import subprocess
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
from config import PURE_VPN_NAME

# import subprocess

init()


def get_recalcul_xy(x, y):
    x_new = x * X_SCREEN_SET / X_SCREEN
    y_new = y * Y_SCREEN_SET / Y_SCREEN

    return x_new, y_new


def get_random_vpn():
    value = random.randint(1, len(PURE_VPN_NAME))
    server = PURE_VPN_NAME.get(value)
    return server


def check_ping_is_ok():
    print('Check PING...')
    hostname = 'bing.com'
    try:
        response = os.system("ping -n 1 " + hostname)
        if response == 0:
            return True
    except:
        # connect_purevpn()
        connect_openvpn()


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
    if OPENVPN == 1:
        load_result = False
        while load_result is False:
            try:
                print('Try to Disconnect OpenVPN')
                rasdial.disconnect()  # Disconnect params_PureVPN first
                check_output("taskkill /im openvpn.exe /F", shell=True)
            except:
                pass

            print('Connect OpenVPN')
            cmd = '"C:\Program Files\OpenVPN\\bin\openvpn.exe"'
            value = random.randint(0, len(CONFIG_IP) - 1)
            print('Random Server: ' + CONFIG_IP[value].strip())
            if 'pointtoserver' in CONFIG_IP[value].strip():
                parameters = ' --client --dev tun --remote ' + CONFIG_IP[value].strip() + ' --port 53' + \
                             ' --proto udp --nobind --persist-key --persist-tun ' \
                             '--tls-auth ressources/params_PureVPN/Wdc.key 1 --ca ca.crt' + \
                             ' --cipher AES-256-CBC --comp-lzo --verb 1 --mute 20 --float --route-method exe' + \
                             ' --route-delay 2 --auth-user-pass ressources/params_PureVPN/auth.txt ' + \
                             '--auth-retry interact' + \
                             ' --explicit-exit-notify 2 --ifconfig-nowarn --auth-nocache '

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


def connect_purevpn():
    if PUREVPN == 1:
        if USER_CONFIG == 'VUNPA':
            load_result = False
            rasdial.disconnect()
            print('Current VPN: ' + str(rasdial.get_current_vpn()))
            while load_result is False:
                rasdial.disconnect()
                sleep(1)
                server = get_random_vpn()

                user = get_params('USER_PUREVPN')
                password = get_params('PASSWORD_PUREVPN')
                rasdial.connect(server, user, password)  # connect to a vpn
                sleep(1)
                if check_ping_is_ok() is True:
                    if check_country_is_ok() is True:
                        if set_zone() is True:
                            load_result = True


def set_screen_resolution():

    try:
        windowList = []
        win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd), hwnd)),
                             windowList)
        cmdWindow = [i for i in windowList if 'onlyclassical' in i[0].lower() or 'classical' in i[0].lower()]

        win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 0, 0, 320, 915, 0)
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
    load_result = False
    counter = 0
    while load_result is False and counter < 2:
        counter += 1
        try:
            key_search = 'onlyclassical'
            sleep(2)
            BROWSER.get('https://encrypted.google.com/#q=' + key_search)
            countdown(2)
            try:
                first_result = ui.WebDriverWait(BROWSER, 5).until(lambda BROWSER:
                                                                   BROWSER.find_element_by_class_name('rc'))
                first_link = first_result.find_element_by_tag_name('a')
                # Open the link in a new tab by sending key strokes on the element
                # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
                first_link.send_keys(Keys.RETURN)
                load_result = True
            except:
                print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"rc\" => Load \"ads-ad\" ' +
                      Style.RESET_ALL)
                try:
                    first_result = ui.WebDriverWait(BROWSER, 5).until(lambda BROWSER:
                                                                      BROWSER.find_element_by_class_name('ads-ad'))
                    first_link = first_result.find_element_by_tag_name('a')
                    first_link.send_keys(Keys.RETURN)
                    load_result = True
                except:
                    print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"ads-ad\" => Reload... ' +
                          Style.RESET_ALL)
                    # switch_main_window()
                    pass
            pass
        except:
            pass

    if counter >= 2:
        try:
            BROWSER.delete_all_cookies()
            BROWSER.quit()
        except:
            pass
        main()

    # Switch tab to the new tab, which we will assume is the next one on the right
    switch_tab()
    random_small_sleep()
    # Take hand the window opener
    # switch_main_window()
    return load_result


def detect_and_click_ads_bottom(url, timing_ads):
    load_result = False
    # switch_main_window()
    try:
        # BROWSER.get(url)
        countdown(5)
        try:
            close_warning = ui.WebDriverWait(BROWSER, 10).until(lambda BROWSER:
                                                                BROWSER.find_element_by_id('spmCloseButton'))
            close_warning.click()
        except:
            pass
        try:
            x, y = get_recalcul_xy(1125, 725)
            print('Try to click Ads: X->' + str(x) + ' Y->' + str(y))
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            sleep(0.25)
            pyautogui.click(x, y)
            load_result = True
        except:
            pass
        # Switch tab to the new tab, which we will assume is the next one on the right
        if load_result is True:
            # switch_tab()
            random_sleep()
            random_mouse_move()
            random_mouse_scroll()
    except:
        pass

    return load_result


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


def get_key_search():
    random_int = random.randint(1, 5000)
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
    global PUREVPN
    global OPENVPN
    global X_SCREEN_SET
    global Y_SCREEN_SET
    global NUMBER_MACHINE
    global X_SCREEN
    global Y_SCREEN
    global KEYWORDS
    global CONFIG_IP
    global COUNTER_TOURS
    global TOTAL_CLICKS_ADS_BOTTOM
    global CONFIG_JSON
    global USER_CONFIG

    with open('OnlyClassical.json') as data_file:
        CONFIG_JSON = load(data_file)

    USER_CONFIG = get_params('USER_CONFIG')
    BOUCLE_SUPER_VIP = int(get_params('BOUCLE_SUPER_VIP'))
    PUREVPN = int(get_params('params_PureVPN'))
    OPENVPN = int(get_params('OpenVPN'))
    X_SCREEN_SET, Y_SCREEN_SET = pyautogui.size()
    X_SCREEN = int(get_params('WIDTH'))
    Y_SCREEN = int(get_params('HEIGHT'))
    CONFIG_IP = tuple(open('ressources/params_PureVPN/list_PureVPN.txt', 'r'))
    # KEYWORDS = tuple(open('ressources\keyword.txt', 'r'))
    COUNTER_TOURS = 0
    TOTAL_CLICKS_ADS_BOTTOM = 0

    # Resize Screen and set Always on TOP
    set_screen_resolution()

    print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'OnlyClassical [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

    # Firefox Parameters
    path_profil = get_path_profile_firefox()
    binary_ff = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

    for z in range(BOUCLE_SUPER_VIP):

        connect_openvpn()  # params_PureVPN

        start_time = time.time()
        # Open Firefox with default profile
        fp = webdriver.FirefoxProfile(path_profil)
        BROWSER = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary_ff)
        BROWSER.maximize_window()

        # Check Whoer once!!!
        print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'Please wait to check Whoer.net... '
              + Style.RESET_ALL)
        load_result = False
        while load_result is False:
            try:
                print('...Check Whoer...')
                BROWSER.get('https://whoer.net/')
                ui.WebDriverWait(BROWSER, 15).until(lambda BROWSER: BROWSER.find_element_by_id('anonym_level'))
                id_level = BROWSER.find_element_by_id('anonym_level').text
                load_result = True
            except:
                connect_openvpn()  # OpenVPN
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
        try:
            # total_key = random.randint(1, 2)
            # for j in range(total_key):
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
        # switch_main_window()

        # Check Ads Bottom
        url = 'http://onlyclassical.org'
        detect_and_click_ads_bottom(url, 15)

        countdown(10)
        random_mouse_scroll()
        random_mouse_move()
        countdown(120)

        COUNTER_TOURS += 1

        #####################
        # Back to the video #
        #####################
        # switch_main_window()
        random_mouse_move()
        print(Fore.LIGHTGREEN_EX + Back.BLACK + '\n[Total timing]' + Style.RESET_ALL + ' ' +
              str(datetime.timedelta(seconds=time.time() - start_time)) + '')
        print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)

        print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
        print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'OnlyClassical [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

        try:
            BROWSER.quit()
        except:
            pass

    print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads] => ' + Style.RESET_ALL
          + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL + '')
    print(Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + 'Press ENTER to close...' + '')
    raw_input()


########################################################################################################################
#                                                Main Program                                                          #
# Arguments:                                                                                                           #
# argv[1]: NUMBER_MACHINE                                                                                              #
#                                                                                                                      #
########################################################################################################################


if __name__ == "__main__":
    main()
