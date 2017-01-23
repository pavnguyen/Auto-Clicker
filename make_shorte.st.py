# for(i = 0; i < $$(".vm-video-title-content").length; i++){ console.log ($$(".vm-video-title-content")[i].href)}
import json
import sys

import requests

if len(sys.argv) > 2:
    debut = int(sys.argv[1])
    fin = int(sys.argv[2])
else:
    print('Please put the First Machine: ')
    debut = int(raw_input())
    print('Please put the Last Machine: ')
    fin = int(raw_input())

for i in range(debut, fin + 1):
    try:
        f = open('ressources\LinksShorter\\' + str(i) + '.txt', 'w+')
        list_links = tuple(open('ressources\LinksYoutube\\' + str(i) + '.txt', 'r'))
        for j in range(0, len(list_links)):
            if "http" in list_links[j]:
                response = requests.put("https://api.shorte.st/v1/data/url", {"urlToShorten": list_links[j].strip()},
                                        headers={"public-api-token": "465fba43219a1e95b506d85b2637db61"})
                print(response.content)
                decoded_response = json.loads(response.content)
                link_shorte_st = decoded_response['shortenedUrl']
                f.write(link_shorte_st + '\n')
    except:
        continue
    f.close()
