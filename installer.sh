#!/usr/bin/env bash

# install wine
sudo add-apt-repository -y ppa:wine/wine-builds
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y --install-recommends wine-staging
sudo apt-get install -y winehq-staging

# prepare wine
sudo apt-get install mesa-utils mesa-utils-extra libgl1-mesa-glx:i386 libgl1-mesa-dev
sudo ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so.1 /usr/lib/i386-linux-gnu/mesa/libGL.so
sudo ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so /usr/lib/i386-linux-gnu/libGL.so
sudo apt-get install winbind

# create and configure wineprefix
cd
WINEPREFIX=$HOME/.wine32office2010 WINEARCH=win32 wine wineboot
wget  https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
chmod +x winetricks
WINEPREFIX=$HOME/.wine32office2010 WINEARCH=win32 ~/winetricks dotnet20 msxml6 corefonts

