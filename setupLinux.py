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
##
from setuptools import setup
import sys,os




script_files = ['AboutDialog.py','MainFrame.py','PrefDialog.py','RabbitHole.py','search.py','SearchPanel.py','request.py','utils.py','AddNewTorrentDialog.py','crawler.py']
plugins = []
images = []
config = []
for i in os.listdir('plugins'):
	plugins.append('plugins/'+i)
for i in os.listdir('images'):
	images.append('images/' + i)
for i in os.listdir('config'):
	config.append('config/'+i)
LaunchScript = "#!/bin/sh\n"
LaunchScript += "cd " + sys.prefix + "/share/rabbithole\n"
LaunchScript += sys.executable + " RabbitHole.py\n"

launchScript = open('rabbithole','w')
launchScript.write(LaunchScript)
launchScript.close()

REQUIRES= ['bs4','ObjectListView','pypubsub','transmissionrpc','bencode']


setup(name='RabbitHole',
      version='DEV',
      description='A simple yet flexible torrent search program that uses plugins.',
      author='Guglielmo De Concini',
      author_email='guglielmo.deconcini@gmail.com',
      url='http://code.google.com/p/rabbithole/',
      license='GPL v3',
      install_requires = REQUIRES,
      scripts=['rabbithole'],
      data_files=[
                  ('share/applications', ['data/rabbithole.desktop']),
                  ('share/rabbithole/images',images ),
                  ('share/rabbithole/config',config ),
                  ('share/rabbithole/plugins',plugins ),
                  ('share/rabbithole',script_files )
                 ]
     )

