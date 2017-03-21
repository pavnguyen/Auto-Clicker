from time import sleep

import tinyurl

try:
    f = open('ressources/URL_bot_views.txt', 'w+')
    urls = tuple(open('ressources/Links_bot_views.txt', 'r'))
    print('Get file...')
    for i in range(0, len(urls)):
        if 'http' in urls[i]:
            link_tinyurl = tinyurl.create_one(urls[i])
            print('Content TinyURL: ' + link_tinyurl + '\n')
            sleep(1)
            f.write(link_tinyurl + '\n')
        else:
            continue
except:
    pass
f.close()
