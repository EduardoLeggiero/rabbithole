arch -i386 python2.7 ./setups/setupMac.py py2app -r images,config,plugins --iconfile images/logo.icns
cp ./setups/stripMac.sh ./dist/
cd ./dist
sh stripMac.sh
rm stripMac.sh
