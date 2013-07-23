Rabbithole
==========
##Purpose

Rabbit Hole is a cross-platform torrent search program

## How to compile

If you want to compile RH, first of all get the latest sources via mercurial, as explained in the _source_ 
section.

#Required Packages=
  * Python (2.7.2)
  * WxWidgets (2.8.12)
  * setup_tools
  * ObjectListView (install via `easy_install` provided by setuptools)
  * BeautifulSoup (install via `easy_install` provided by setuptools)
  * pypubsub (install via `easy_install` provided by setuptools)
  * py2app (MacOSX only, install via `easy_install` provided by setuptools)
  * py2exe (Windowsonly, install via `easy_install` provided by setuptools)
#MacOsx
Open terminal and cd into the `rabbithole` folder obtained via mercurial.
Then execute: `sh compileMac.sh` 
Compiled binary should be in dist folder.
Execute `sh clean.sh` to clean all compilation files, or manually delete _build_ and _dist_ folders.

#Windows
Open _cmd_ and cd into the `rabbithole` folder obtained via mercurial.
Then execute `python setupWin.py py2exe`.
Compiled binary should be in dist folder.
Manually delete _build_ and _dist_ folders to get rid of compiled data.

#Linux 
Open _cmd_ and cd into the `rabbithole` folder obtained via mercurial.
Then execute 

`python setupLinux.py install --root=/`.

##Settings panel options

#General Tab
  * *Default Plugin:* sets the default plugin to search with.
  * *Request Timeout:* sets the time, in seconds, after wich a connection timeout error is raised. If you have 
a slow connection or querying a slow responding server, you might want increase this one.
  * *Pages:* Maximum number of web pages to fetch when fetiching results from a site. 

#Super Search Tab
The switch button lets you decide which plugins are to be included or not in the Super Search

#Transmission Tab
If you are familiar with the Transmission RPC interface this section should be pretty self-explanatory.
Leave `localhost` in the host field if Transmission and RH are being executed on the same machine.
