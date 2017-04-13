# for(i = 0; i < $$(".vm-video-title-content").length; i++){ console.log ($$(".vm-video-title-content")[i].href)}
import sys
try:
    import tinyurl
except:
    import TinyURL as tinyurl

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
        f = open('ressources/LinksPopAds/' + str(i) + '.txt', 'w+')
        list_links = tuple(open('ressources/LinksYoutube/' + str(i) + '.txt', 'r'))
        for j in range(0, len(list_links)):
            if "http" in list_links[j]:
                link = list_links[j].strip()
                link_tinyurl = tinyurl.create_one(link)
                link_popads = link_tinyurl + '#' + link
                f.write(link_popads + '\n')
    except:
        continue
    f.close()
