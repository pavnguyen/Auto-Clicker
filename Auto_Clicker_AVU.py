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
from platform import uname
from time import sleep

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
from config import SCREEN_RESOLUTION  # config.py
from config import USER_PASS
from config import PURE_VPN_NAME
from config import PIA_VPN_NAME
from screen_resolution import ScreenRes
import subprocess
import shutil
import errno
import smtplib

init()


def send_email_alert():
    try:
        fromaddr = 'vu.nomos@gmail.com'
        toaddrs = 'vunguyen.xbt@gmail.com'
        text = uname()[1] + ' could not connect!!!'
        msg = 'Subject: {}\n\n{}'.format('AutoClicker', text)
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


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("parent.lock", "lock", ".parentlock"))
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            pass


def restore_profile():
    profile_number = str(random.randint(0, len(os.listdir('ressources\Profiles\\')) - 1))
    user_name = getpass.getuser()
    path_profil = 'C:\Users\\' + user_name + '\AppData\Roaming\Mozilla\Firefox\Profiles\\'
    profil_name = os.listdir(path_profil)[0]
    folder = path_profil + profil_name

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            pass

    try:
        shutil.rmtree(folder)
    except:
        pass
    print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'Profile: ' + profile_number + Style.RESET_ALL)
    if not os.path.exists(folder):
        copyanything('ressources\Profiles\\' + profile_number, folder)


def get_tinyurl_clip(channel):
    load_result = False
    while load_result is False:
        try:
            links_tinyurl = tuple(open('ressources/LinksTinyURL/' + str(channel) + '.txt', 'r'))
            random_int = random.randint(0, len(links_tinyurl) - 1)
            if 'http' in links_tinyurl[random_int].strip() and 'undefined' not in links_tinyurl[random_int].strip():
                yt_tinyurl = links_tinyurl[random_int].strip()
                load_result = True
        except:
            pass
    return yt_tinyurl


def get_title_clip(channel):
    global TITLE_YOUTUBE
    load_result = False
    search_youtube = 'https://www.youtube.com/results?search_query='
    while load_result is False:
        try:
            links_tinyurl = tuple(open('ressources/TitlesYoutube/' + str(channel) + '.txt', 'r'))
            random_int = random.randint(1, len(links_tinyurl) - 1)
            if 'undefined' not in links_tinyurl[random_int].strip() and links_tinyurl[random_int].strip() is not None \
                    and links_tinyurl[random_int].strip() != '':
                TITLE_YOUTUBE = links_tinyurl[random_int].strip()
                load_result = True
        except:
            pass
    return search_youtube + TITLE_YOUTUBE


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


def connect_purevpn():
    if PUREVPN == 1:
        load_result = False
        rasdial.disconnect()
        division = round(float(TOTAL_CHANNEL) / len(USER_PASS))
        print('Current VPN: ' + str(rasdial.get_current_vpn()))
        counter_connect = 0
        while load_result is False and counter_connect < 4:
            if counter_connect >= 2:
                send_email_alert()
            counter_connect += 1
            rasdial.disconnect()
            sleep(1)

            if USER_CONFIG == 'VUNPA' and NUMBER_MACHINE <= TOTAL_CHANNEL and ADS_BOTTOM == 1 and NUMBER_MACHINE <= 15:
                server = get_random_vpn(PURE_VPN_NAME)

                if NUMBER_MACHINE <= division:
                    value = 1
                elif division < NUMBER_MACHINE <= TOTAL_CHANNEL - (TOTAL_CHANNEL / len(USER_PASS)):
                    value = 2
                else:
                    value = 3
                user = USER_PASS.get(value)[0]
                password = USER_PASS.get(value)[1]
            elif USER_CONFIG == 'VUNPA' and NUMBER_MACHINE >= 20:
                division = NUMBER_MACHINE % 20
                if division == 0:
                    value = 1
                elif division == 1:
                    value = 2
                elif division == 2:
                    value = 3
                else:
                    value = random.randint(1, 3)
                server = get_random_vpn(PURE_VPN_NAME)
                user = USER_PASS.get(value)[0]
                password = USER_PASS.get(value)[1]
            elif USER_CONFIG != 'VUNPA' or (USER_CONFIG == 'VUNPA' and ADS_BOTTOM == 1) or ADS_BOTTOM == 0:
                server = get_random_vpn(PIA_VPN_NAME)
                user = 'x3569491'
                password = 'rUTPQnvnv7'

                # server = 'HMA'
                # user = 'avestergrd'
                # password = 'vESsRzDB'

            rasdial.connect(server, user, password)  # connect to a vpn
            sleep(1)
            if check_ping_is_ok() is True:
                # if check_country_is_ok() is True:
                if set_zone() is True:
                        load_result = True


def connect_openvpn_purevpn():
    if OPENVPN == 1:
        load_result = False
        while load_result is False:
            try:
                print('Try to Disconnect OpenVPN')
                rasdial.disconnect()  # Disconnect params_PureVPN first
                subprocess.check_output("taskkill /im openvpn.exe /F", shell=True)
            except:
                pass

            print('Connect OpenVPN')
            cmd = '"C:/Program Files/OpenVPN/bin/openvpn.exe"'
            value = random.randint(0, len(CONFIG_IP_PURE) - 1)
            print('Random Server: ' + CONFIG_IP_PURE[value].strip())
            if 'pointtoserver' in CONFIG_IP_PURE[value].strip():
                parameters = ' --client --dev tun --remote ' + CONFIG_IP_PURE[value].strip() + ' --port 53' + \
                             ' --proto udp --nobind --persist-key --persist-tun ' \
                             '--tls-auth ressources/params_PureVPN/Wdc.key 1 --ca ressources/params_PureVPN/ca.crt' + \
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


def connect_openvpn():
    if OPENVPN == 1 or ADS_BOTTOM == 0:
        # if NUMBER_MACHINE > TOTAL_CHANNEL or ADS_BOTTOM == 0 or PUREVPN == 0:
        load_result = False
        counter_connect = 0
        while load_result is False and counter_connect < 4:
            if counter_connect >= 2:
                send_email_alert()
            counter_connect += 1
            if sys.platform == 'win32':
                try:
                    print('Try to Disconnect OpenVPN')
                    rasdial.disconnect()  # Disconnect params_PureVPN first
                    subprocess.check_output("taskkill /im openvpn.exe /F", shell=True)
                except:
                    pass

                subprocess.check_output('ipconfig /release', shell=True)
                subprocess.check_output('ipconfig /renew', shell=True)

            print('Connect OpenVPN')
            if sys.platform == 'win32':
                cmd = '"C:/Program Files/OpenVPN/bin/openvpn.exe"'
            else:
                cmd = '/etc/openvpn/openvpn'
            if ADS_BOTTOM == 0:
                value = random.randint(0, len(CONFIG_IP_VIEW) - 1)
            else:
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
            else:
                parameters = ' --tls-client --client --dev tun --link-mtu 1500' \
                             ' --remote ' + CONFIG_IP[value].strip() + \
                             ' --proto udp --port 1197' \
                             ' --lport 53 --persist-key --persist-tun --ca ressources/params_PIA/data/ca.crt ' \
                             '--comp-lzo --mute 3' \
                             ' --auth-user-pass ressources/params_PIA/data/auth.txt' \
                             ' --reneg-sec 0 --route-method exe --route-delay 2' \
                             ' --verb 3 --log c:/log.txt --status c:/stat.db 1 --auth-nocache' \
                             ' --crl-verify ressources/params_PIA/data/crl.pem ' \
                             '--remote-cert-tls server --block-outside-dns' \
                             ' --cipher aes-256-cbc --auth sha256'

            cmd += parameters
            try:
                subprocess.Popen(cmd)
                print('Please wait to connect to OpenVPN...')
                countdown(8)
            except:
                pass

            if check_ping_is_ok() is True:
                # if check_country_is_ok() is True:
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
    switch_main_window()
    return load_result


def search_youtube(url):
    switch_main_window()
    load_result = False
    count = 0
    while load_result is False and count <= 1:
        count += 1
        try:
            BROWSER.get(url)
            random_mouse_move()
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + TITLE_YOUTUBE + Style.RESET_ALL)
            xpath_search = "//a[@title=" + "'" + TITLE_YOUTUBE + "']"
            first_link = ui.WebDriverWait(BROWSER, 5).until(lambda BROWSER: BROWSER.find_element_by_xpath(xpath_search))
            first_link.send_keys(Keys.RETURN)
            load_result = True
        except:
            pass
    return load_result


def click_button_skipads():
    try:
        first_result = ui.WebDriverWait(BROWSER, 3).until(
            lambda BROWSER: BROWSER.find_element_by_class_name('videoAdUiSkipButton'))
        x, y = get_recalcul_xy(980, 559)
        random_sleep()
        pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
        pyautogui.click(x, y)
    except:
        pass


def detect_and_click_ads_bottom(timing_ads):
    global TOTAL_CLICKS_ADS_SKIPS
    global DETECTED_ADDISPLAY

    load_result = False
    switch_main_window()
    try:
        # SKIP ADS
        # try:
        #     first_result = ui.WebDriverWait(BROWSER, 20).until(
        #         lambda BROWSER: BROWSER.find_element_by_class_name('annotation'))
        #     print('...Annotation checked')
        #     try:
        #         first_result.click()
        #     except:
        #         try:
        #             x, y = get_recalcul_xy(323, 556)
        #             pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
        #             random_small_sleep()
        #             pyautogui.click(323, 556)
        #             print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.BRIGHT + 'annotation 2' + Style.RESET_ALL)
        #             TOTAL_CLICKS_ADS_SKIPS += 1
        #             load_result = True
        #         except:
        #             pass
        #     switch_tab()
        #     random_mouse_move()
        #     switch_main_window()
        #     random_mouse_move()
        #     pyautogui.hotkey('alt', 'esc')
        #
        #     replay_clip()
        #     click_button_skipads()
        #     random_mouse_move()
        # except:
        try:
            x, y = get_recalcul_xy(330, 600)
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            first_result = ui.WebDriverWait(BROWSER, 20).until(
                lambda BROWSER: BROWSER.find_element_by_class_name('iv-promo-txt'))  # ('iv-promo-contents'))
            try:
                first_result.click()
                print('click 2')
            except:
                pyautogui.click(323, 556)
                print('click 3')
                pass
            TOTAL_CLICKS_ADS_SKIPS += 1
            load_result = True
            print(
                Back.BLACK + Fore.LIGHTBLUE_EX + Style.BRIGHT + 'Class \"iv-promo-txt\" => ' + Style.RESET_ALL +
                Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)
            switch_tab()
            random_mouse_move()
            random_small_sleep()
            switch_main_window()
            random_mouse_move()

            pyautogui.hotkey('alt', 'esc')
            replay_clip()
            click_button_skipads()
        except:
            try:
                x, y = get_recalcul_xy(330, 600)
                pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
                first_result = ui.WebDriverWait(BROWSER, 5).until(
                    lambda BROWSER: BROWSER.find_element_by_class_name('videoAdUiVisitAdvertiserLinkText'))
                print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.BRIGHT +
                      'Class \"videoAdUiVisitAdvertiserLinkText\" => ' +
                      Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT +
                      '[DETECTED]' + Style.RESET_ALL)
                try:
                    pyautogui.moveTo(330, 600, random.random(), pyautogui.easeOutQuad)
                    pyautogui.click(330, 576)
                    print('click 4')
                    TOTAL_CLICKS_ADS_SKIPS += 1
                    load_result = True
                except:
                    pyautogui.click(330, 576)
                    pass
                switch_tab()
                random_mouse_move()
                switch_main_window()
                random_mouse_move()

                pyautogui.hotkey('alt', 'esc')
                replay_clip()
                click_button_skipads()
                random_mouse_move()
            except:
                pass

        # ADS BOTTOM
        random_mouse_move()
        x, y = get_recalcul_xy(624, 559)  # just for fun
        pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
        DETECTED_ADDISPLAY = 1

        try:
            if get_info_length_youtube(BROWSER.current_url) / 60 > 10:
                print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'Wait n times to click SECOND ads' +
                      Style.RESET_ALL)
                countdown(45)
        except:
            pass
        if load_result is False:
            try:
                first_result = ui.WebDriverWait(BROWSER, 35).until(lambda BROWSER:
                                                                   BROWSER.find_element_by_class_name(
                                                                       'adDisplay'))
                first_link = first_result.find_element_by_tag_name('a')
                first_link.send_keys(Keys.CONTROL + Keys.RETURN)

                print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Class \"adDisplay\" => ' + Style.RESET_ALL +
                      Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)
                load_result = True
            except:
                try:
                    first_result = ui.WebDriverWait(BROWSER, 5).until(lambda BROWSER:
                                                                      BROWSER.find_element_by_id('AdSense'))
                    first_link = first_result.find_element_by_tag_name('a')
                    first_link.send_keys(Keys.CONTROL + Keys.RETURN)

                    print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Id \"AdSense\" => ' + Style.RESET_ALL +
                          Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[DETECTED]' + Style.RESET_ALL)
                    load_result = True
                    DETECTED_ADDISPLAY = 0
                    print(Fore.LIGHTRED_EX + 'Error: adDisplay => Load \"AdSense\"' + Style.RESET_ALL)
                except:
                    try:
                        first_result = ui.WebDriverWait(BROWSER, 5).until(
                            lambda BROWSER: BROWSER.find_element_by_class_name('adDisplay'))
                        first_link = first_result.find_element_by_tag_name('a')
                        first_link.send_keys(Keys.CONTROL + Keys.RETURN)

                        print(
                            Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Class 2 \"adDisplay\" => ' +
                            Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT +
                            '[DETECTED]' + Style.RESET_ALL)

                        load_result = True
                        DETECTED_ADDISPLAY = 0
                    except:
                        print(Fore.LIGHTRED_EX + 'Error: AdSense => Reload clip!!!' + Style.RESET_ALL)
                        pass
                    pass
                    # Switch tab to the new tab, which we will assume is the next one on the right
            if load_result is True:
                switch_tab()
                random_mouse_move()
                random_small_sleep()
                random_mouse_scroll()
                switch_main_window()
                replay_clip()
            else:
                click_ads_right()
    except:
        pass

    return load_result


def click_ads_right():
    if ADS_RIGHT == 1 or ADS_BOTTOM == 0:
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT)
        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT)
        print('>> Ads Right >> Try to Click Ads RIGHT')
        print(Style.RESET_ALL)

        try:
            x, y = get_recalcul_xy(1230, 205)
            pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
            pyautogui.keyDown('ctrl')
            pyautogui.click()
            pyautogui.keyUp('ctrl')
            switch_tab()
            random_mouse_move()
            countdown(20)
        except:
            try:
                pyautogui.keyUp('ctrl')
            except:
                pass

    try:
        pyautogui.keyUp('ctrl')
        random_mouse_move()
    except:
        pyautogui.keyUp('ctrl')
        pass
    switch_main_window()


def replay_clip():
    try:
        print('-> Mouse move to Clip')
        x, y = get_recalcul_xy(540, 450)
        pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
        get_position_mouse()
        sleep(0.25)
        try:
            pyautogui.click(x, y)
        except:
            pass
        print('-> Mouse click to REPLAY')
        random_mouse_move()
        random_mouse_move()
    except:
        pass


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

        # region_name = load(urlopen(link))['region_name']
        # print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Region] => ' + region_name + Style.RESET_ALL)
        #
        # city = load(urlopen(link))['city']
        # print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[City] => ' + city + Style.RESET_ALL)
        #
        # time_zone = load(urlopen(link))['time_zone']
        # print(Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '[Time Zone] => ' + time_zone + Style.RESET_ALL)

        # Google API service form Vu.nomos
        link = 'https://maps.googleapis.com/maps/api/timezone/json?location=' + str(latitude) + ',' + \
               str(longitude) + '&timestamp=' + timestamp + '&key=AIzaSyAC2ESW2jOFDdABT6hZ4AKfL7U8jQRSOKA'
        timeZoneId = load(urlopen(link))['timeZoneId']

        zone_to_set = LIST_TIME_ZONE.get(timeZoneId)
        print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + 'Synchronize ' + zone_to_set + Style.RESET_ALL)
        if zone_to_set.strip() != '':
            subprocess.check_output("tzutil /s " + '"' + zone_to_set + '" ', shell=True)
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


def main(optional):
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
    global X_SCREEN
    global Y_SCREEN
    global KEYWORDS
    global CONFIG_IP
    global CONFIG_IP_VIEW
    global CONFIG_IP_PURE
    global CONFIG_JSON
    global USER_CONFIG
    global COUNTER_TOURS
    global TOTAL_CLICKS_ADS_BOTTOM
    global TYPE_CLICKER
    global GOOGLE_SEARCH

    with open('config_auto_clicker.json') as data_file:
        CONFIG_JSON = load(data_file)

    TYPE_CLICKER = get_params('TYPE_CLICKER')
    USER_CONFIG = get_params('USER_CONFIG')
    if optional == 1:
        ADS_BOTTOM = int(get_params('ADS_BOTTOM'))
    else:
        ADS_BOTTOM = 0
    ADS_RIGHT = int(get_params('ADS_RIGHT'))
    GOOGLE_SEARCH = int(get_params('GOOGLE_SEARCH'))
    CLOSE_ADS_BOTTOM = int(get_params('CLOSE_ADS_BOTTOM'))
    TOTAL_CHANNEL = int(get_params('TOTAL_CHANNEL'))
    PUREVPN = int(get_params('PureVPN'))
    OPENVPN = int(get_params('OpenVPN'))
    if ADS_BOTTOM == 1:
        BOUCLE_SUPER_VIP = int(get_params('BOUCLE_SUPER_VIP'))
    else:
        PUREVPN = 0
        OPENVPN = 1
        BOUCLE_SUPER_VIP = 1

    X_SCREEN = int(get_params('WIDTH'))
    Y_SCREEN = int(get_params('HEIGHT'))
    X_SCREEN_SET, Y_SCREEN_SET = pyautogui.size()
    CONFIG_IP = tuple(open('ressources/params_PIA/list_PIA.txt', 'r'))
    CONFIG_IP_VIEW = tuple(open('ressources/params_PIA/list_PIA_VIEW.txt', 'r'))
    KEYWORDS = tuple(open('ressources/keyword.txt', 'r'))

    # Resize Screen and set Always on TOP
    set_screen_resolution()

    print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'Auto Clicker [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

    print(
        Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + "Number Machine: " + str(NUMBER_MACHINE) + '' + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + "Total Channel: " +
          str(TOTAL_CHANNEL) + '' + Style.RESET_ALL)
    if ADS_BOTTOM == 0:
        print(Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + '-----------[MODE] VIEW ONLY----------' +
              Style.RESET_ALL)

    # Firefox Parameters
    if sys.platform == 'win32':
        restore_profile()
        path_profil = get_path_profile_firefox()
        binary_ff = FirefoxBinary(r'C:/Program Files (x86)/Mozilla Firefox/firefox.exe')

    if TYPE_CLICKER == 'DAILY' and ADS_BOTTOM == 1:
        BOUCLE_SUPER_VIP = 1

    for z in range(BOUCLE_SUPER_VIP):
        if (NUMBER_MACHINE > TOTAL_CHANNEL and PUREVPN != 1) or ADS_BOTTOM == 0 or PUREVPN == 0 or optional == 0:
            connect_openvpn()  # OpenVPN
        else:
            connect_purevpn()  # params_PureVPN

        for i in range(NUMBER_MACHINE, TOTAL_CHANNEL + NUMBER_MACHINE):
            start_time = time.time()
            if ADS_BOTTOM == 1:
                print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' + Style.RESET_ALL
                      + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL + '')
                print(Fore.LIGHTGREEN_EX + Back.BLACK + ' ' * 12 + '[Ads SKIP included] => ' + Style.RESET_ALL
                      + Fore.LIGHTYELLOW_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_SKIPS) + Style.RESET_ALL + '')

            # Open Firefox with default profile
            if i == NUMBER_MACHINE or ADS_BOTTOM == 1 or ADS_BOTTOM == 0:
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

            #################
            # Google Search #
            #################
            if ADS_BOTTOM == 1 and GOOGLE_SEARCH == 1:
                try:
                    total_key = random.randint(1, 2)
                    for j in range(total_key):
                        loaded_google = search_google()  # Search Google with keywords

                        print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Search Key] => ' + Style.RESET_ALL +
                              Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + '[ OK ]' + Style.RESET_ALL)
                        random_small_sleep()
                except:
                    print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Search Key] => ' + Style.RESET_ALL +
                          Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + 'FAILED!!!' + Style.RESET_ALL)
                    pass

                print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' + Style.RESET_ALL
                      + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL + '')
                print(Fore.LIGHTGREEN_EX + Back.BLACK + ' ' * 12 + '[Ads SKIP included] => ' + Style.RESET_ALL
                      + Fore.LIGHTYELLOW_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_SKIPS) + Style.RESET_ALL + '')
            #####################
            # Detect Ads Bottom #
            #####################

            file_channel = i

            if i <= TOTAL_CHANNEL:
                file_channel = i
            else:
                file_channel = (i + TOTAL_CHANNEL) % TOTAL_CHANNEL

            if file_channel == 0:
                file_channel = TOTAL_CHANNEL

            switch_main_window()

            # Check Ads Bottom
            found_ads_bottom = False
            if ADS_BOTTOM == 1:
                counter = 0
                timing_ads = random.randint(23, 34)
                while found_ads_bottom is False and counter < 2:
                    try:
                        url = get_title_clip(str(file_channel))
                        print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'URL Ads >> ' + Style.RESET_ALL +
                              Back.BLACK + Fore.LIGHTWHITE_EX + url + Style.RESET_ALL)
                        result_search_youtube = search_youtube(url)

                        if result_search_youtube is False:
                            url = get_tinyurl_clip(str(file_channel))
                            BROWSER.get(url)
                        counter += 1
                        print("...Test Ads Bottom: " + str(counter))
                        found_ads_bottom = detect_and_click_ads_bottom(timing_ads)
                        if found_ads_bottom is True:
                            TOTAL_CLICKS_ADS_BOTTOM += 1
                            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + '[Ads Bottom] => ' +
                                  Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT +
                                  '[FOUND & CLICKED]' + Style.RESET_ALL)
                            print(
                                Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' +
                                Style.RESET_ALL + Fore.LIGHTGREEN_EX + Back.BLACK +
                                str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL)
                            print(
                                Fore.LIGHTGREEN_EX + Back.BLACK + ' ' * 12 + '[Ads SKIP included] => ' +
                                Style.RESET_ALL + Fore.LIGHTYELLOW_EX + Back.BLACK +
                                str(TOTAL_CLICKS_ADS_SKIPS) + Style.RESET_ALL)
                    except:
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

            COUNTER_TOURS += 1

            # View AFTER detect and click real ads

            if ADS_BOTTOM == 0:
                total_key = random.randint(5, 7)
                for j in range(total_key):
                    try:
                        switch_main_window()
                        url = get_title_clip(str(file_channel))
                        result_search_youtube = search_youtube(url)
                        if result_search_youtube is False:
                            url = get_tinyurl_clip(str(file_channel))
                            BROWSER.get(url)

                        countdown(15)
                        print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'URL VIEW: ' + str(j) + ' >> ' +
                              Style.RESET_ALL + Back.BLACK + Fore.LIGHTWHITE_EX + url + '' + Style.RESET_ALL)
                        click_button_skipads()
                        random_mouse_move()
                        if j % total_key == 0:
                            click_ads_right()
                    except:
                        pass

            #####################
            # Back to the video #
            #####################
            switch_main_window()
            if ADS_BOTTOM == 1:
                try:
                    sleep(1)
                    current_url = BROWSER.current_url
                    print('Current url:' + current_url)
                except:
                    print('Current Url is not found!')
                    pass

                if current_url is not None:
                    try:
                        wait_time = get_info_length_youtube(current_url) - random.randint(59, 69)
                        if wait_time < 0 or wait_time > 220:
                            wait_time = random.randint(105, 115)
                    except:
                        wait_time = random.randint(105, 115)

                    # Try to close Ads
                    if CLOSE_ADS_BOTTOM == 1:
                        random_close = random.randint(0, 1)
                        if random_close == 1:
                            try:
                                if DETECTED_ADDISPLAY == 0:
                                    x, y = get_recalcul_xy(990, 503)
                                else:
                                    x, y = get_recalcul_xy(845, 536)
                                print(Fore.LIGHTYELLOW_EX + Back.BLACK + 'Try to close Ads: X->' +
                                      str(x) + ' Y->' + str(y) + Style.RESET_ALL)
                                pyautogui.moveTo(x, y, random.random(), pyautogui.easeOutQuad)
                                sleep(0.25)
                                try:
                                    pyautogui.click(x, y)
                                except:
                                    pass
                            except:
                                pass

            random_mouse_move()

            if ADS_BOTTOM == 1:
                ###################
                # Click Ads RIGHT #
                ###################
                try:
                    print(Fore.LIGHTYELLOW_EX + Back.BLACK + '[Search key] => ' + Style.RESET_ALL
                          + Fore.LIGHTGREEN_EX + Back.BLACK + str(total_key) + Style.RESET_ALL)
                except:
                    pass
                print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + '[Duration to click ads]' + Style.RESET_ALL +
                      Back.BLACK + Fore.LIGHTWHITE_EX + ' ' +
                      str(datetime.timedelta(seconds=time.time() - start_time)) + '' + Style.RESET_ALL)
                print(Fore.LIGHTYELLOW_EX + Back.BLACK + ' ' * 12 + '[Click Ads Bottom] => ' + Style.RESET_ALL
                      + Fore.LIGHTGREEN_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_BOTTOM) + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX + Back.BLACK + ' ' * 12 + '[Ads SKIP included] => ' + Style.RESET_ALL
                      + Fore.LIGHTYELLOW_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_SKIPS) + Style.RESET_ALL)

            print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + ' ' * 9 + 'FINISH -> Tours -> ' +
                  Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + str(COUNTER_TOURS) + '' + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)

            # click_ads_right()
            if found_ads_bottom is True:
                countdown(wait_time)
                # elif ADS_BOTTOM == 0:
                # countdown(random.randint(15, 35))

            print(Fore.LIGHTGREEN_EX + Back.BLACK + '\n[Total timing]' + Style.RESET_ALL + ' ' +
                  str(datetime.timedelta(seconds=time.time() - start_time)) + '')
            print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)

            print(Back.BLACK + Fore.LIGHTBLUE_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'Auto Clicker [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
            print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

            try:
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
        print(Fore.LIGHTGREEN_EX + Back.BLACK + ' ' * 12 + '[Ads SKIP included] => ' + Style.RESET_ALL
              + Fore.LIGHTYELLOW_EX + Back.BLACK + str(TOTAL_CLICKS_ADS_SKIPS) + Style.RESET_ALL + '')

    if TYPE_CLICKER != 'DAILY':
        print(Back.LIGHTWHITE_EX + Fore.LIGHTRED_EX + Style.BRIGHT + 'VuNguyen.XBT@Gmail.com ...' + '')
        # raw_input()


########################################################################################################################
#                                                Main Program                                                          #
# Arguments:                                                                                                           #
# argv[1]: NUMBER_MACHINE                                                                                              #
#                                                                                                                      #
########################################################################################################################


if __name__ == "__main__":
    COUNTER_TOURS = 0
    TOTAL_CLICKS_ADS_BOTTOM = 0
    TOTAL_CLICKS_ADS_SKIPS = 0
    global NUMBER_MACHINE
    if len(sys.argv) > 1:
        NUMBER_MACHINE = int(sys.argv[1])
    else:
        print(Back.BLACK + Fore.LIGHTWHITE_EX + ' ' * 3 + '[ Please enter the Machine Number: ]' +
              Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX)
        print(Style.RESET_ALL)
        NUMBER_MACHINE = str(raw_input())

    for i in range(0, 100):
        if NUMBER_MACHINE <= 19:
            main(0)
        else:
            main(1)
