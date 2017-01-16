# Copy all links to input.txt => output.txt with link Tinyurl#linkYoutube
# for(i = 0; i < $$(".vm-video-title-content").length; i++){ console.log ($$(".vm-video-title-content")[i].href)}
import tinyurl

f = open('ressources\LinksPopAds\\output.txt', 'w+')
list_links = tuple(open('ressources\LinksPopAds\\input.txt', 'r'))
for i in range(0, len(list_links)):
    if "http" in list_links[i]:
        link = list_links[i].strip()
        link_tinyurl = tinyurl.create_one(link)
        link_popads = link_tinyurl + '#' + link
        f.write(link_popads + '\n')
f.close()
