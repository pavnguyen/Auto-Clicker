######################################################################
# HOW TO USE
# [1] Use this function in console Chrome to get all clips
# for(i = 0; i < $$(".vm-video-title-content").length; i++){ console.log ($$(".vm-video-title-content")[i].innerHTML)}
# [2] Save this content to ressources\TitlesYoutube\{your_channel_number}.txt like 1.txt, 2.txt, 3.txt,...
# [3] Config file config.py with Params['TOTAL_CHANNEL]
# [4] Check result at the directory ressources\LinksTinyURL\
######################################################################

import sys
from time import sleep

import bs4
import requests
import tinyurl

from config import PARAMS

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

# Search clip in Google
link_search_google = 'https://encrypted.google.com/search?q='

if len(sys.argv) > 2:
    debut = int(sys.argv[1])
    fin = int(sys.argv[2])

for i in range(debut, fin + 1):
    try:
        f = open('ressources\LinksTinyURL\\' + str(i) + '.txt', 'w+')
        list_name_youtube_channel = tuple(open('ressources\TitlesYoutube\\' + str(i) + '.txt', 'r'))
        print('Get file...')
        sleep(1)
        for j in range(1, len(list_name_youtube_channel)):
            try:
                # Get clip to search with Google
                name_clip = list_name_youtube_channel[j]
                name_clip = name_clip.strip('\n')
                url = link_search_google + name_clip
                print('Clip: ' + url + '\n')
                sleep(1)
                res = requests.get(url)
                sleep(1)
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
            except:
                continue
    except:
        continue
    f.close()
