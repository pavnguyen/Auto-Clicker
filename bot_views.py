import os
import random
import subprocess
import sys
import time
from subprocess import check_output

import requests
from selenium import webdriver

import rasdial


def connect_openvpn():
    CONFIG_IP = tuple(open('ressources/config_ip.txt', 'r'))
    load_result = False
    while load_result is False:
        if sys.platform == 'win32':
            try:
                print('Try to Disconnect OpenVPN')
                rasdial.disconnect()  # Disconnect PureVPN first
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
            parameters = ' --client --dev tun --tun-mtu 1500 --proto udp --remote ' \
                         + CONFIG_IP[value].strip() + \
                         ' --port 1198 --resolv-retry infinite --nobind --persist-key --persist-tun' \
                         ' --cipher aes-128-cbc --auth sha1 --tls-client --remote-cert-tls server' \
                         ' --auth-user-pass data/auth.txt --comp-lzo --verb 1 --reneg-sec 0' \
                         ' --crl-verify data\crl.rsa.2048.pem' \
                         ' --auth-nocache' \
                         ' --block-outside-dns' \
                         ' --ca data\ca.rsa.2048.crt'

        cmd += parameters
        try:
            subprocess.Popen(cmd)
            print('Please wait to connect to OpenVPN...')
            countdown(8)
        except:
            pass

        print('Check PING...')
        hostname = 'bing.com'
        try:
            response = os.system("ping -n 1 " + hostname)
            if response == 0:
                load_result = True
        except:
            connect_openvpn()


def countdown(timing):
    while timing >= 0:
        mins, secs = divmod(timing, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        timing -= 1
        print('Please wait...' + timeformat)


def OpenUrl(url):
    r = requests.get(url)
    # r.close()


# refresh = raw_input("Enter refresh rate(seconds) : ")
urls = tuple(open('ressources/Links_bot_views.txt', 'r'))
BROWSER = webdriver.Firefox()

# connect_openvpn()
for j in range(50):
    for i in range(0, len(urls) - 1):
        print("*" * 60)
        print('Tour: ' + str(j + 1) + ' --- ' + str(i + 1) + ' -> ' + urls[i])
        print("*" * 60)
        BROWSER.get(urls[i])
        try:
            MAIN_WINDOW = BROWSER.current_window_handle
        except:
            pass

        countdown(15)

print('Press ENTER to close...' + '')
raw_input()
