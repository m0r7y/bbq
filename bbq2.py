import subprocess
import time
from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener

from bs4 import BeautifulSoup

cookie_jar = CookieJar()
opener = build_opener(HTTPCookieProcessor(cookie_jar))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0'),
                     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                     ('Connection', 'Keep-Alive')]

temp_url = []
l_url = ''
with open('title', 'r') as f:
    files = [x.rstrip() for x in f.readlines()]
    f.close()

for file in files:
    search_dic = {'search_query': file}
    search_que = urlencode(search_dic).encode('utf-8')

    soup = BeautifulSoup(opener.open(
        'https://www.youtube.com/results', search_que), 'html.parser')

    links = soup.find_all('a',
                          {'class': 'yt-simple-endpoint style-scope ytd-video-renderer'})
    for link in links:
        temp_url.append(link.get('href'))
    l_url += 'https://www.youtube.com' + temp_url[0] + ' '
    temp_url = []
    time.sleep(1)

cmd = 'youtube-dl -f best -x --audio-format mp3 -i ' + l_url.rstrip()
subprocess.Popen(cmd, shell=True)
