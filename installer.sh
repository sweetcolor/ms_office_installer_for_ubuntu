#!/usr/bin/env bash

prefix=wine32office


while [ "$1" != "" ]; do
    case $1 in
        -c | --config-directory )
            shift
            config_directory=$1
            ;;
        -o | --office-installer )
            shift
            office_installer=$1
            ;;
        -p | --prefix )
            shift
            prefix=$1
            ;;
        -h | --help )
            usage
            exit
            ;;
        * )
            usage
            exit 1
    esac
    shift
done
echo ${prefix}
echo ${config_directory}
if [[ ${office_installer:${#office_installer}-3:3} == "iso" ]]
then
    if ! [ -d /media/${USER}/iso ]
    then
        echo 'sdfsdf'
        echo $USER
        echo $HOME
        sudo mkdir /media/${USER}/iso
    fi
elif [[ ${office_installer:${#office_installer}-3:3} == "exe" ]]
then
    echo 'exe'
else
    echo 'else'
fi
echo ${office_installer}
## install wine
#sudo add-apt-repository -y ppa:wine/wine-builds
#sudo dpkg --add-architecture i386
#sudo apt-get update
#sudo apt-get install -y --install-recommends wine-staging
#sudo apt-get install -y winehq-staging
#
## prepare wine
#sudo apt-get install mesa-utils mesa-utils-extra libgl1-mesa-glx:i386 libgl1-mesa-dev
#sudo ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so.1 /usr/lib/i386-linux-gnu/mesa/libGL.so
#sudo ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so /usr/lib/i386-linux-gnu/libGL.so
#sudo apt-get install winbind
#
## create and configure wineprefix
#cd
#WINEPREFIX=$HOME/.wine32office2010 WINEARCH=win32 wine wineboot
#wget  https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
#chmod u+x winetricks
#WINEPREFIX=$HOME/.wine32office2010 WINEARCH=win32 ~/winetricks dotnet20 msxml6 corefonts
#WINEPREFIX=$HOME/.wine32office2010 WINEARCH=win32 wine
