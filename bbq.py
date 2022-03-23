import re
import subprocess
import time
from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener

cookie_jar = CookieJar()
opener = build_opener(HTTPCookieProcessor(cookie_jar))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0'),
                     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                     ('Connection', 'Keep-Alive')]

with open('title', 'r') as f:
    files = [x.rstrip() for x in f.readlines()]
    f.close()

l_url = ''
# source_url = open('source', 'w')

for file in files:
    search_dic = {'search_query': file}
    search_que = urlencode(search_dic).encode('utf-8')

    resp = opener.open('https://www.youtube.com/results', search_que)
    resp_str = resp.read().decode('utf-8')
    # return tuple
    resp_list = re.findall(r'<a href="(.*)" class=.* title="(.*)" aria-describedby.* Duration:.*>', resp_str,
                           re.IGNORECASE)

    # source_url.write(urljoin('https://www.youtube.com/', resp_list[0][0])+'\n')
    l_url += 'https://www.youtube.com' + resp_list[0][0] + ' '
    time.sleep(1)

# source_url.close()
cmd = 'youtube-dl -f best -i -x --audio-format mp3 ' + l_url.rstrip()
subprocess.Popen(cmd, shell=True)
