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
                USE_IP = CONFIG_IP_VIEW   
            else:
                USE_IP = CONFIG_IP
                
            value = random.randint(0, len(USE_IP) - 1)
            print('Random Server: ' + USE_IP[value].strip())
            if 'privateinternetaccess' in USE_IP[value].strip():
                parameters = ' --client --dev tun --proto udp --remote ' \
                             + USE_IP[value].strip() + \
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
                             ' --remote ' + USE_IP[value].strip() + \
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
    # try:
    #     windowList = []
    #     win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd), hwnd)),
    #                          windowList)
    #     cmdWindow = [i for i in windowList if 'auto clicker' in i[0].lower() or 'openvpn' in i[0].lower()]
    #     win32gui.SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 1395, 0, 320, 915, 0)
    # except:
    #     pass


def search_youtube(url):
    load_result = False
    count = 0
    while load_result is False and count <= 1:
        count += 1
        try:
            BROWSER.get(url)
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
        try:
            first_result.click()
        except:
            pass
    except:
        pass


def random_sleep():
    r = random.randint(3, 5)
    sleep(r)


def random_small_sleep():
    r = random.randint(1, 2)
    sleep(r)



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
    global ADS_BOTTOM
    global ADS_RIGHT
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

    with open('config_auto_clicker.json') as data_file:
        CONFIG_JSON = load(data_file)

    USER_CONFIG = get_params('USER_CONFIG')
    if optional == 1:
        ADS_BOTTOM = int(get_params('ADS_BOTTOM'))
    else:
        ADS_BOTTOM = 0
    ADS_RIGHT = int(get_params('ADS_RIGHT'))
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
    print(Fore.LIGHTWHITE_EX + '=' * 8 + '  ' + 'Phantom Viewer [AVU]' + '  ' + '=' * 7 + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTRED_EX + Style.NORMAL + '=' * 37 + Style.RESET_ALL)

    print(
        Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + "Number Machine: " + str(NUMBER_MACHINE) + '' + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTCYAN_EX + Style.BRIGHT + "Total Channel: " +
          str(TOTAL_CHANNEL) + '' + Style.RESET_ALL)
    print(Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + '-----------[MODE] VIEW ONLY----------' +
            Style.RESET_ALL)


    for z in range(BOUCLE_SUPER_VIP):
        if (NUMBER_MACHINE > TOTAL_CHANNEL and PUREVPN != 1) or ADS_BOTTOM == 0 or PUREVPN == 0 or optional == 0:
            connect_openvpn()  # OpenVPN
        else:
            connect_purevpn()  # params_PureVPN

        for i in range(NUMBER_MACHINE, TOTAL_CHANNEL + NUMBER_MACHINE):
            start_time = time.time()

            file_channel = i

            if i <= TOTAL_CHANNEL:
                file_channel = i
            else:
                file_channel = (i + TOTAL_CHANNEL) % TOTAL_CHANNEL

            if file_channel == 0:
                file_channel = TOTAL_CHANNEL

            # Open Firefox with default profile
            if sys.platform == 'win32':
                # fp = webdriver.FirefoxProfile(path_profil)
                # BROWSER = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary_ff)

                ########################## TEST PHANTOM JS #############################################
                headers = { 'Accept':'*/*',
                            'Accept-Encoding':'gzip, deflate, sdch',
                            'Accept-Language':'en-US,en;q=0.8',
                            'Cache-Control':'max-age=0',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
                            }
                for key, value in enumerate(headers):
                    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value                                
                    BROWSER = webdriver.PhantomJS()
                    BROWSER.set_window_size(1120, 550)
            print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + ' ' * 9 + 'FINISH -> Tours -> ' +
                  Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + str(COUNTER_TOURS) + '' + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)
                            
            total_key = random.randint(5, 7)
            COUNTER_TOURS += 1
            for j in range(total_key):
                try:
                    url = get_title_clip(str(file_channel))
                    result_search_youtube = search_youtube(url)
                    if result_search_youtube is False:
                        url = get_tinyurl_clip(str(file_channel))
                        BROWSER.get(url)

                    countdown(15)
                    print(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'URL VIEW: ' + str(j) + ' >> ' +
                            Style.RESET_ALL + Back.BLACK + Fore.LIGHTWHITE_EX + url + '' + Style.RESET_ALL)
                    click_button_skipads()
                    countdown(random.randint(30, 90))
                except:
                    pass

            print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)
            print(Back.BLACK + Fore.LIGHTGREEN_EX + Style.BRIGHT + ' ' * 9 + 'FINISH -> Tours -> ' +
                  Style.RESET_ALL + Back.BLACK + Fore.LIGHTYELLOW_EX + str(COUNTER_TOURS) + '' + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + '.' * 37 + Style.RESET_ALL)



########################################################################################################################
#                                                Main Program                                                          #
# Arguments:                                                                                                           #
# argv[1]: NUMBER_MACHINE                                                                                              #
#                                                                                                                      #
########################################################################################################################


if __name__ == "__main__":
    global NUMBER_MACHINE
    COUNTER_TOURS = 0    
    if len(sys.argv) > 1:
        NUMBER_MACHINE = int(sys.argv[1])
    else:
        print(Back.BLACK + Fore.LIGHTWHITE_EX + ' ' * 3 + '[ Please enter the Machine Number: ]' +
              Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX)
        print(Style.RESET_ALL)
        NUMBER_MACHINE = str(raw_input())

    for i in range(0, 10000):
        main(0)
