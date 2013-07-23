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
import re

class TorrentListItem(object):

    def __init__(self,category, name, size ,seeders, leechers,url,magneturl,plugin):
        self.category = category
        self.name = name
        self.size = size
        self.seeders = seeders
        self.leechers = leechers
        self.url = url
        self.magneturl= magneturl
        self.plugin = plugin

def formatSize(byteCount):
    for (cutoff, label) in [(1024*1024*1024, "GB"), (1024*1024, "MB"), (1024, "KB")]:
        if byteCount >= cutoff:
            return "%.1f %s" % (byteCount * 1.0 / cutoff, label)
    if byteCount == 1:
        return "1 byte"
    else:
        return "%d bytes" % byteCount

def deformatSize(size):
    #print size
    decoder = {'B':1,
            'KB':1024,
            'MB':1024*1024,
            'GB':1024*1024*1024,
            'kB':1024,
            'Bytes':1}
    
    bits = size.split(" ")
    if len(bits)!= 2:
        bits = re.findall('([0-9]*\.?[0-9]+)([GKMTB]+)',size)[0]
    #print bits
    for key in decoder:
        if key == bits[1]:
            return int(float(bits[0].replace(',',''))* decoder[key])#Pure se sbaja de quarche bit a noi che ce frega :-)?

