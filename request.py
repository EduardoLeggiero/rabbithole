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

from urllib2 import Request as request
from urllib2 import urlopen
from urllib import pathname2url
import StringIO
import gzip,zlib

def __decode (resp):
    encoding = resp.info().get("Content-Encoding")    
    if encoding in ('gzip', 'x-gzip', 'deflate'):
        content = resp.read()
        if encoding == 'deflate':
            data = StringIO.StringIO(zlib.decompress(resp))
        else:
            data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
        return data
    return resp

def doRequest(url,headers,timeout):
    
    headers_full = {'Accept-Encoding': 'gzip,deflate'}
    headers_full.update(headers)

    req = request(url , headers=headers_full)

    resp = urlopen(req, timeout=timeout)

    return __decode(resp)



