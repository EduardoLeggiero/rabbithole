## This file is part of Rabbit Hole.

##     Rabbit Hole is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.

##     Rabbit Hole is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with Rabbit Hole.  If not, see <http://www.gnu.org/licenses/>.


import bs4
from urllib2 import Request as request
from urllib2 import urlopen
from urllib import pathname2url

def crawler(url,settings,headers,timeout):
    
    DEBUG= True
    req = request(url,headers=headers)	
    page = urlopen(req,timeout=timeout)
    soup = bs4.BeautifulSoup(page)  
    
    if DEBUG:
        print "RabbitHole: Crawler fetched data  on " + req.get_full_url()
            
    l = []
    for i in soup.findAll(settings['tag'],attrs=settings['attrs']):
            
        if "attrs_len" in settings and len(i.attrs) != settings["attrs_len"]:
            continue

        if settings['method'] == 'text':
            if "decode" in settings:
                l.append(re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', i.text))
            else:
                l.append(i.text)
        elif settings['method'] == 'attr':
            l.append(i[settings["attr"]])

    if "index" in settings:
        url_out = l[int(settings['index'])]
    else:
        url_out = l[0]

    if "manipulate" in settings:

        if "regexp" in settings["manipulate"]: 
            l[i] = re.findall(settings["manipulate"]["regexp"],url_out)[0]
        if "to_replace" in settings["manipulate"]:
            l[i] = str(url_out).replace(settings["manipulate"]["to_replace"],settings["manipulate"]["replace_with"])

    if DEBUG:
        print l
        print "Crawler: List len=" + str(len(l))
        print "Crawler: URL=" + str(url_out)  

    return url_out
                               
