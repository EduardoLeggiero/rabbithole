from distutils.core import setup
import py2exe
import sys,os
import glob
sys.path.append("C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")
data_files = []
manifest=open("pythonw.exe.manifest","r").read()

def find_data_files(source,target,patterns):

   if glob.has_magic(source) or glob.has_magic(target):
       raise ValueError("Magic not allowed in src, target")
   ret = {}
   for pattern in patterns:
       pattern = os.path.join(source,pattern)
       for filename in glob.glob(pattern):
           if os.path.isfile(filename):
               targetpath = os.path.join(target,os.path.relpath(filename,source))
               path = os.path.dirname(targetpath)
               ret.setdefault(path,[]).append(filename)
   return sorted(ret.items())

excludes = ['tcl',
            'Tkconstants',
            'Tkinter']
setup(
   name="HologramEditor",
   version="1.0",
   options = {'py2exe': {'optimize': 2,'bundle_files': 1,'dll_excludes' : ['w9xpopen.exe'],"packages": ['pubsub','ObjectListView']}},
   description="Rabbit Hole",
   author="Guglielmo De Concini",
   windows=[{'script': "RabbitHole.py",'other_resources': [(24,1,manifest)],"icon_resources": [(1, "images/logo.ico")]}],
   data_files=data_files+find_data_files('.','',[
       'images/*',
       'plugins/*',
       'config/*']),
   zipfile = None,
)
   

