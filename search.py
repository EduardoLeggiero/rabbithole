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
from urllib import quote_plus
import json
from utils import *
from threading import Thread
import re
import wx
from pubsub import pub
from request import doRequest

DEBUG = False
PRINTURL = False
SAFE = True

class SearchThread(Thread):

    def __init__(self,query , category , name, plugins, pages, timeout):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.name = name
        self.query = query
        self.category = category
        self.plugins = plugins
        self.pages = pages
        self.timeout = timeout
        self.start()
        
    def run(self):
        table = []
        data = {}

        for i,plugin_name in enumerate(self.plugins):

            try:
                plugin_file = open('plugins/' + plugin_name +'.json')
                plugin = json.loads(plugin_file.read())
                plugin_file.close()
            except StandardError, ex:
                wx.CallAfter(pub.sendMessage,"error",msg="Sorry, Rabbit Hole couldn't open plugin "  + plugin_name + " ,reason:" + str(ex)) 
                return

            try:
                data =  self.__kayak(self.query,self.category if self.category else plugin['categories']["All"],plugin,self.pages,self.timeout,plugin_name)
            except StandardError, ex:
                wx.CallAfter(pub.sendMessage,"error",msg="Sorry, Rabbit Hole couldn't connect to "  + plugin_name + " ,reason:" + str(ex)) 
                continue

            prefix = ''

            if 'url_filter' in plugin:
                prefix+='[T]'
            if 'magnet_url_filter' in plugin:
                prefix+='[M]'
            if len(self.plugins) > 1:
                prefix+='['+plugin_name+'] -- '
                

            for i,title in enumerate(data['titles_filter']):
                table.append(TorrentListItem(data['category_filter'][i],
                                             prefix + title,
                                             deformatSize(data['size_filter'][i]),
                                             int(data['seed_filter'][i]) if data['seed_filter'][i] else 0,
                                             int(data['leech_filter'][i]) if data['leech_filter'][i] else 0,
                                             data['url_filter'][i] if 'url_filter' in plugin else None,
                                             data['magnet_url_filter'][i] if 'magnet_url_filter' in plugin else None,
                                             plugin_name ))
        self.__SendData(table)

    def __kayak(self,query,category,plugin,pages,timeout,plugin_name):

        page_counter = 0

        data = {}
        for op in plugin['operations']:
            data[op] = []

        for page_no in range(plugin["page_rules"]["start"], pages * plugin["page_rules"]["step"] + 1, plugin["page_rules"]["step"]):

            elements_counter = -1

            page_counter += 1

            if page_counter > pages:
                break

            urldata = plugin["pattern"].replace('[query]', quote_plus(query)).replace('[category]', str(category)).replace('[page]', str(page_no))
            wx.CallAfter(pub.sendMessage, "status", status="[" + plugin_name + "] Retrieving data on page " + str(page_counter))
            if PRINTURL:
                print("Fetched data on " + plugin['base_search_url'] + urldata)
            page = doRequest(plugin['base_search_url'] + urldata,plugin['headers'],timeout)
            wx.CallAfter(pub.sendMessage, "status", status="[" + plugin_name + "] Parsing data on page " + str(page_counter))
            soup = bs4.BeautifulSoup(page)
            del page


            output = {}   

            for op in plugin['operations']:

                if "fixed_value" in plugin[op]:
                        output[op] = [plugin[op]["fixed_value"]]*plugin["page_rules"]["max_items"]
                        continue

                output[op] = [] 

                for i in soup.findAll(plugin[op]['tag'], attrs=plugin[op]['attrs']):

                    if "attrs_len" in plugin[op] and len(i.attrs) != plugin[op]["attrs_len"]:
                            continue

                    if plugin[op]['method'] == 'text':
                        if "decode" in plugin[op]:
                            output[op].append(re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', i.text))
                        else:
                            output[op].append(i.text)
                    elif plugin[op]['method'] == 'attr':
                        output[op].append(i[plugin[op]["attr"]])

                if "chipper" in plugin[op]:
                    output[op] = output[op][plugin[op]["chipper"]["start"]:]
                    pos = 0
                    for i,val in  enumerate(output[op]):
                        if i%plugin[op]["chipper"]["step"] == 0:
                            output[op][pos] = val
                            pos+=1
                    output[op] = output[op][:min(pos,plugin["page_rules"]["max_items"])]

                if "manipulate" in plugin[op]:
                    for i,item in enumerate(output[op]):
                        if "regexp" in plugin[op]["manipulate"]: 
                            try:
                                output[op][i] = re.findall(plugin[op]["manipulate"]["regexp"], item)[0]
                            except StandardError, rex:
                                if DEBUG:
                                    wx.CallAfter(pub.sendMessage,"error",msg="Regexping error on "+ plugin_name + ": " + str(rex))
                                    print("Error while regexping(manipulate)[" + op+ "] " + item)
                                output[op][i] = ''

                        if "to_replace" in plugin[op]["manipulate"]:
                            for j,toReplace in enumerate(plugin[op]["manipulate"]["to_replace"]):
                                output[op][i] = output[op][i].replace(toReplace, plugin[op]["manipulate"]["replace_with"][j])
                        
                        if "prefix" in plugin[op]["manipulate"]:
                            output[op][i] = plugin[op]["manipulate"]["prefix"] + output[op][i]

                        if "suffix" in plugin[op]["manipulate"]:
                            output[op][i] += plugin[op]["manipulate"]["suffix"]


                if len(output[op]) < elements_counter or elements_counter < 0:
                    elements_counter = len(output[op])
                

            if SAFE:
                for key in output.keys():
                    output[key] = output[key][:elements_counter]

            if DEBUG:
                print("--------DUMP-----------")
                for key in output:
                    print("-------------[" + str(key) + "]")
                    print(str(output[key]))
                    print("-------------[" + str(len(output[key])) + "]")

            for op in plugin['operations']:
                data[op].extend(output[op])

            if len(output["titles_filter"]) < plugin["page_rules"]["max_items"]:
                break

        return data

    def __SendData(self,output):
        wx.CallAfter(pub.sendMessage, "status", status="[" + self.name + "] Search completed")
        wx.CallAfter(pub.sendMessage, "Search completed", data=output ,query=self.query,plugin=self.name )
                               
        
