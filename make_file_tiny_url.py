######################################################################
# HOW TO USE
# [1] Use this function in console Chrome to get all clips
# for(i = 0; i < $$(".vm-video-title-content").length; i++){ console.log ($$(".vm-video-title-content")[i].innerHTML)}
# [2] Save this content to ressources\TitlesYoutube\{your_channel_number}.txt like 1.txt, 2.txt, 3.txt,...
# [3] Config file config.py with Params['TOTAL_CHANNEL]
# [4] Check result at the directory ressources\LinksTinyURL\
######################################################################

import bs4
import requests
import tinyurl
import sys
from config import PARAMS
from time import sleep

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def get_params(param):  # param = 'TOTAL_CHANNEL'
    for key in PARAMS:
        if param in key:
            return PARAMS[key]


# Search clip in Google
link_search_google = 'https://encrypted.google.com/search?q='

if len(sys.argv) > 1:
    nbr_channel = int(sys.argv[1])
else:
    nbr_channel = get_params('TOTAL_CHANNEL')

for i in range(1, nbr_channel + 1):
    f = open('ressources\LinksTinyURL\\' + str(i) + '.txt', 'w+')
    list_name_youtube_channel = tuple(open('ressources\TitlesYoutube\\' + str(i) + '.txt', 'r'))
    print('Get file...')
    sleep(1)
    for j in range(1, len(list_name_youtube_channel)):
        # Get clip to search with Google
        name_clip = list_name_youtube_channel[j]
        name_clip = name_clip.strip('\n')
        url = link_search_google + name_clip
        print('Clip: ' + url + '\n')
        sleep(1)
        res = requests.get(url)
        print('Please wait 3s to get request...\n')
        sleep(3)
        res.raise_for_status()
        sleep(1)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        linkElems = soup.select('.r a')
        sleep(1)
        # Find out correct link <-> Youtube
        for index in range(5):
            if (name_clip + ' - YouTube' == linkElems[index].getText()) or \
                    (name_clip[:67] + ' ...' == linkElems[index].getText() + ' ...'):
                url_ytb = 'https://www.google.com' + linkElems[index].get('href')
                print('Youtube: ' + url_ytb + '\n')
                sleep(1)
                link_tinyurl = tinyurl.create_one(url_ytb)
                print('Content TinyURL: ' + link_tinyurl + '\n')
                sleep(1)
                break
        f.write(link_tinyurl + '\n')
    f.close()
