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
from config import PARAMS
from config import SCREEN_RESOLUTION  # config.py
from config import USER_PASS
from config import VPN_NAME
from list_timezone import LIST_TIME_ZONE
from screen_resolution import ScreenRes

init()


def get_tinyurl_clip(channel):
    link = tuple(open('ressources\LinksTinyURL\\' + str(channel) + '.txt', 'r'))
    random_int = random.randint(0, 9)
    return link[random_int]


def get_random_vpn():
    value = random.randint(1, len(VPN_NAME))
    server = VPN_NAME.get(value)
    return server


def connect_pure_vpn(refresh):
    if get_params('PureVPN') == 1:
        if refresh is True:
            rasdial.disconnect()
            sleep(2)
        while rasdial.is_connected() is False:
            print('Current VPN: ' + str(rasdial.get_current_vpn()))
            rasdial.disconnect()
            sleep(3)
            server = get_random_vpn()
            value = random.randint(1, 2)
            user = USER_PASS.get(value)[0]
            password = USER_PASS.get(value)[1]
            rasdial.connect(server, user, password)  # connect to a vpn
            sleep(3)


def get_random_resolution():
    value = random.randint(1, len(SCREEN_RESOLUTION))
    width = SCREEN_RESOLUTION.get(value)[0]
    height = SCREEN_RESOLUTION.get(value)[1]
    return width, height


def get_recalcul_xy(x, y, x_screen_set, y_screen_set):
    x_screen = get_params('WIDTH')
    y_screen = get_params('HEIGHT')

    x_new = x * x_screen_set / x_screen
    y_new = y * y_screen_set / y_screen

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
        cmdWindow = [i for i in windowList if "auto" in i[0].lower()]

        win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 360, 0, 670, 120, 0)
    except:
        pass


def get_params(param):  # param = 'TOTAL_CHANNEL'
    for key in PARAMS:
        if param in key:
            return PARAMS[key]


def switch_main_window(browser, main_window):
    try:
        browser.switch_to.window(main_window)
    except:
        print('Error: Browser can not take main window => Re-take main window ')
        browser.switch_to.window(main_window)
        pass


def switch_tab(browser):
    # Switch tab to the new tab, which we will assume is the next one on the right
    try:
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    except:
        try:
            print('Error: Switch tab to the new tab => Re-witch Tab')
            browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        except:
            pass
        pass


def search_google(browser, main_window):
    result_search = False
    count_search = 0
    while result_search is False and count_search < 3:
        count_search += 1
        try:
            key_search = get_key_search()
            sleep(3)
            browser.get('https://encrypted.google.com/#q=' + key_search)
            sleep(3)

            try:
                first_result = ui.WebDriverWait(browser, 15).until(lambda browser:
                                                                   browser.find_element_by_class_name('rc'))
                first_link = first_result.find_element_by_tag_name('a')
                # Open the link in a new tab by sending key strokes on the element
                # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
                first_link.send_keys(Keys.CONTROL + Keys.RETURN)
                result_search = True
            except:
                print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"rc\" => Load \"ads-ad\" ' +
                      Style.RESET_ALL)
                try:
                    first_result = ui.WebDriverWait(browser, 15).until(lambda browser:
                                                                       browser.find_element_by_class_name('ads-ad'))
                    first_link = first_result.find_element_by_tag_name('a')
                    first_link.send_keys(Keys.CONTROL + Keys.RETURN)
                    result_search = True
                except:
                    print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT + 'Error: \"ads-ad\" => Reload... ' +
                          Style.RESET_ALL)
                    pass
            pass
        except:
            pass
    # Switch tab to the new tab, which we will assume is the next one on the right
    switch_tab(browser)
    random_small_sleep()
    # Take hand the window opener
    switch_main_window(browser, main_window)
    return result_search


def detect_and_click_ads_bottom(browser, url, timing_ads):
    load_url = False
    try:
        browser.get(url)
        sleep(3)
        try:
            first_result = ui.WebDriverWait(browser, timing_ads).until(lambda browser:
                                                                       browser.find_element_by_class_name('adDisplay'))
            first_link = first_result.find_element_by_tag_name('a')
            first_link.send_keys(Keys.CONTROL + Keys.RETURN)

            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Class \"adDisplay\" => ' + Style.RESET_ALL +
                  Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)

            # Switch tab to the new tab, which we will assume is the next one on the right
            switch_tab(browser)

            random_sleep()
            random_mouse_scroll()
            random_mouse_move()

            load_url = True
        except:
            print(Fore.LIGHTRED_EX + 'Error: adDisplay => Load \"AdSense\"' + Style.RESET_ALL)
            try:
                first_result = ui.WebDriverWait(browser, timing_ads).until(lambda browser:
                                                                           browser.find_element_by_id('AdSense'))
                first_link = first_result.find_element_by_tag_name('a')
                first_link.send_keys(Keys.CONTROL + Keys.RETURN)

                print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Id \"AdSense\" => ' + Style.RESET_ALL +
                      Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)

                # Switch tab to the new tab, which we will assume is the next one on the right
                switch_tab(browser)

                random_sleep()
                random_mouse_scroll()
                random_mouse_move()
                load_url = True
            except:
                print(Fore.LIGHTRED_EX + 'Error: AdSense => Reload clip!!!' + Style.RESET_ALL)
                pass
            pass
    except:
        pass
    return load_url


def click_ads_right():
    if get_params('ADS_RIGHT') == 1:
        try:
            x_screen_set, y_screen_set = pyautogui.size()
            x, y = get_recalcul_xy(1330, 270, x_screen_set, y_screen_set)
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            pyautogui.keyDown('ctrl')
            pyautogui.click()
            pyautogui.keyUp('ctrl')
            sleep(1)
            x, y = get_recalcul_xy(1335, 423, x_screen_set, y_screen_set)
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
    print('-> Mouse move to Clip')
    x_screen_set, y_screen_set = pyautogui.size()
    x, y = get_recalcul_xy(540, 300, x_screen_set, y_screen_set)
    pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
    get_position_mouse()
    sleep(0.25)
    pyautogui.click(x, y)
    print('-> Mouse click to REPLAY')
    random_mouse_move()


def random_sleep():
    r = random.randint(5, 9)
    sleep(r)


def random_small_sleep():
    r = random.randint(1, 3)
    sleep(r)


def random_mouse_move():
    for i in range(0, 5):
        x = random.randint(5, 1024)
        y = random.randint(8, 768)
        pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
        pyautogui.moveRel(x, y, random.random(), pyautogui.easeOutQuad)
        random_small_sleep()


def random_mouse_scroll():
    for i in range(0, 2):
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
    keywords = tuple(open('ressources\keyword.txt', 'r'))
    random_int = random.randint(1, 5500)
    print(Fore.LIGHTYELLOW_EX + Back.BLACK + '>> Keywords >> ' + Style.RESET_ALL + Fore.LIGHTGREEN_EX +
          Back.BLACK + keywords[random_int] + Style.RESET_ALL)
    return keywords[random_int].strip('')


def get_name_clip(channel):
    channel = tuple(open('ressources\LinksYoutube\\' + str(channel) + '.txt', 'r'))
    random_int = random.randint(1, 10)
    print(Fore.LIGHTGREEN_EX + Back.BLACK + '[Clip] => ' + Style.RESET_ALL + Fore.LIGHTGREEN_EX +
          Back.BLACK + channel[random_int] + Style.RESET_ALL)
    return channel[random_int]


def get_zone(timeZoneId):
    for key in LIST_TIME_ZONE:
        if timeZoneId in key:
            return LIST_TIME_ZONE[key]


def set_zone():
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

    # Google API service
    link = 'https://maps.googleapis.com/maps/api/timezone/json?location=' + str(latitude) + ',' + str(longitude) \
           + '&timestamp=' + timestamp + '&key=AIzaSyAC2ESW2jOFDdABT6hZ4AKfL7U8jQRSOKA'  # GOOGLE API from vu.nomos
    timeZoneId = load(urlopen(link))['timeZoneId']

    zone_to_set = get_zone(timeZoneId)
    check_output("tzutil /s " + '"' + zone_to_set + '" ', shell=True)

    print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[IP] => ' + ip + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Region] => ' + region_name + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[City] => ' + city + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Time Zone] => ' + time_zone + Style.RESET_ALL)


def countdown(timing):
    while timing:
        mins, secs = divmod(timing, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(Fore.LIGHTCYAN_EX + Back.BLACK + Style.BRIGHT + 'Please wait ... ' + timeformat +
              ' to finish this JOB!!!' + Style.RESET_ALL, end='\r')
        time.sleep(1)
        timing -= 1


########################################################################################################################
#                                                Main Program                                                          #
# Arguments:                                                                                                           #
# argv[1]: number_machine                                                                                              #
#                                                                                                                      #
########################################################################################################################


# Resize Screen and set Always on TOP
set_screen_resolution()

print('' + Back.BLACK + Fore.BLUE + Style.NORMAL + '=' * 80 + Style.RESET_ALL)
print(' ' * 22 + 'Auto Browser SUPER VIP - AVU')
print(Back.BLACK + Fore.RED + Style.NORMAL + '=' * 80)

if len(sys.argv) > 1:
    number_machine = int(sys.argv[1])
else:
    number_machine = 1

nbr_channel = get_params('TOTAL_CHANNEL')

print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + "Number Machine: " + str(number_machine) + '' + Style.RESET_ALL)

# PureVPN
connect_pure_vpn(True)

set_zone()  # Synchro Time Zone with VPN server IP , country, zone, etc...

# Firefox Parameters
path_profil = get_path_profile_firefox()
binary_ff = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

counter_tours = 0
counter_total_click_ads_bottom = 0
for z in range(get_params('BOUCLE_SUPER_VIP')):

    if z != 0:
        connect_pure_vpn(True)

    for i in range(number_machine, nbr_channel + number_machine):

        # Pure VPN
        connect_pure_vpn(False)

        print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 47 + '[Counter Click Ads Bottom] => ' + Style.RESET_ALL
              + Fore.LIGHTGREEN_EX + Back.BLACK + str(counter_total_click_ads_bottom) + Style.RESET_ALL + '')

        start_time = time.time()

        # Open Firefox with default profile
        fp = webdriver.FirefoxProfile(path_profil)
        browser = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary_ff)
        browser.maximize_window()

        # Check Whoer once!!!
        if i == number_machine:
            print(Back.BLACK + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Please wait to check Whoer.net... '
                  + Style.RESET_ALL)
            w_load = False
            while w_load is False:
                try:
                    print('Check Whoer INPUT')
                    browser.get('https://whoer.net/')
                    print('Check Whoer OUTPUT')
                    sleep(3)
                    ui.WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_id('anonym_level'))
                    id_level = browser.find_element_by_id('anonym_level').text
                    w_load = True
                except:
                    pass
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Status] => ' + Style.RESET_ALL +
                  Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + id_level + '' + Style.RESET_ALL)

            browser.delete_all_cookies()

        # Save the window opener
        try:
            main_window = browser.current_window_handle
        except:
            main_window = browser.current_window_handle
            pass

        #################
        # Google Search #
        #################
        try:
            total_key = random.randint(1, 3)
            for j in range(total_key):
                loaded_google = search_google(browser, main_window)  # Search Google with keywords

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
        switch_main_window(browser, main_window)

        print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 47 + '[Counter Click Ads Bottom] => ' + Style.RESET_ALL
              + Fore.LIGHTGREEN_EX + Back.BLACK + str(counter_total_click_ads_bottom) + Style.RESET_ALL + '')

        file_channel = i

        if i <= nbr_channel:
            file_channel = i
        else:
            file_channel = (i + nbr_channel) % nbr_channel

        if file_channel == 0:
            file_channel = nbr_channel

        url = get_tinyurl_clip(str(file_channel))
        url = url.strip('\n')

        print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '>> URL >> ' + Style.RESET_ALL +
              Back.BLACK + Fore.LIGHTWHITE_EX + url + '' + Style.RESET_ALL)

        # Check Ads Bottom
        ads_bottom = False
        counter_boucle = 0
        timing_ads = random.randint(25, 39)
        while ads_bottom is False and counter_boucle < 3:
            try:
                counter_boucle += 1
                print("Test Ads Bottom: " + str(counter_boucle))
                switch_main_window(browser, main_window)
                ads_bottom = detect_and_click_ads_bottom(browser, url, timing_ads)

                if ads_bottom is True:
                    counter_total_click_ads_bottom += 1
                    print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Ads Bottom] => ' +
                          Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT +
                          '[FOUNDED & CLICKED]' + Style.RESET_ALL)
                    print(
                        Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 47 + '[Counter Click Ads Bottom] => ' +
                        Style.RESET_ALL + Fore.LIGHTGREEN_EX + Back.BLACK +
                        str(counter_total_click_ads_bottom) + Style.RESET_ALL)
            except:
                continue

        if ads_bottom is False:
            continue

        counter_tours += 1

        #####################
        # Back to the video #
        #####################

        switch_main_window(browser, main_window)

        if ads_bottom is True:
            replay_clip()  # Click and replay clip

        ###################
        # Click Ads RIGHT #
        ###################

        click_ads_right()

        print(Fore.LIGHTYELLOW_EX + Back.BLACK + '[Search key] => ' + Style.RESET_ALL
              + Fore.LIGHTGREEN_EX + Back.BLACK + str(total_key) + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + '[Duration to click ads]' + Style.RESET_ALL +
              Back.BLACK + Fore.LIGHTWHITE_EX + ' ' +
              str(datetime.timedelta(seconds=time.time() - start_time)) + '' + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 47 + '[Counter Click Ads Bottom] => ' + Style.RESET_ALL
              + Fore.LIGHTGREEN_EX + Back.BLACK + str(counter_total_click_ads_bottom) + Style.RESET_ALL)

        print(Fore.LIGHTMAGENTA_EX + '*' * 80 + Style.RESET_ALL)
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + ' ' * 30 + 'FINISH -> Tours -> ' +
              Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + str(counter_tours) + '' +
              Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + '*' * 80 + Style.RESET_ALL)

        if ads_bottom is True:
            try:
                sleep(1)
                current_url = browser.current_url
                print('Current url:' + current_url)
            except:
                print('Current Url is didn\'t found!')
                pass

            if current_url is not None:
                try:
                    wait_time = get_info_length_youtube(current_url) - random.randint(40, 50)
                except:
                    wait_time = random.randint(150, 180)
                countdown(wait_time)  # Wait n minutes to view

        print(Fore.LIGHTGREEN_EX + Back.BLACK + '\n[Total timing]' + Style.RESET_ALL + ' ' +
              str(datetime.timedelta(seconds=time.time() - start_time)) + '')
        print(Fore.LIGHTMAGENTA_EX + '*' * 80 + Style.RESET_ALL)

        try:
            browser.delete_all_cookies()
            browser.quit()
        except:
            pass

    try:
        browser.delete_all_cookies()
        browser.quit()
    except:
        pass

print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 47 + '[Counter Click Ads Bottom] => ' + Style.RESET_ALL
      + Fore.LIGHTGREEN_EX + Back.BLACK + str(counter_total_click_ads_bottom) + Style.RESET_ALL + '')
print(Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + 'Press ENTER to close...' + '')
raw_input()
