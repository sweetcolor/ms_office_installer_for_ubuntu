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
        -v | --version )
            shift
            version=$1
            ;;
        -h | --help )
            # TODO installer.sh help
            usage
            exit
            ;;
        * )
            usage
            exit 1
    esac
    shift
done
function run_installer {
    if [[ ${office_installer:${#office_installer}-3:3} == "iso" ]]
    then
        iso_mount_folder=/media/${USER}/iso
        if [ ! -d ${iso_mount_folder} ]
        then
            echo "creating ${iso_mount_folder} directory"
            sudo mkdir ${iso_mount_folder}
        fi
        echo "mount ${office_installer} in ${iso_mount_folder} directory"
        sudo mount -t iso9660 -o loop ${office_installer} ${iso_mount_folder}
        setup_file=${iso_mount_folder}/setup.exe
    elif [[ ${office_installer:${#office_installer}-3:3} == "exe" ]]
    then
        setup_file=${office_installer}
    else
        echo 'setup file not recognized'
    fi
    WINEPREFIX=$HOME/.${prefix} wine ${setup_file}
    WINEPREFIX=~/.wine32 ./winetricks msxml6=native riched20=native gdiplus=native
}

function install_wine {
    sudo apt-get install -y wine-mono wine-gecko
    sudo dpkg --add-architecture i386
    if [[ ${version} =~ [0-9].[0-9] ]]
    then
        sudo add-apt-repository ppa:ubuntu-wine/ppa
        sudo apt-get update
        # Maybe will need
        # sudo apt-get upgrade
        sudo apt-get install wine${version} winetricks
        winetricks='winetricks'
    elif [ ${version} == '-b' ] || [ ${version} == '--build' ]
    then
        sudo add-apt-repository -y ppa:wine/wine-builds
        sudo apt-get update
        sudo apt-get install -y --install-recommends wine-staging
        sudo apt-get install -y winehq-staging
        wget  https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
        chmod u+x winetricks
        winetricks='~/winetricks'
    else
        echo 'wrong version'
        exit
    fi
}

function prepare_wine {
    # install OpenGL
    sudo apt-get install -y mesa-utils mesa-utils-extra libgl1-mesa-glx:i386 libgl1-mesa-dev
    # need for x64
    sudo ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so.1 /usr/lib/i386-linux-gnu/mesa/libGL.so
    sudo ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so /usr/lib/i386-linux-gnu/libGL.so
    # Install winbind. Office installation stops midway if this is not done
    sudo apt-get install -y winbind
}

function create_wineprefix {
    WINEPREFIX=$HOME/.${prefix} WINEARCH=win32 wine wineboot
    WINEPREFIX=$HOME/.${prefix} ${winetricks} dotnet20 msxml6 corefonts
}

install_wine
prepare_wine
create_wineprefix
run_installer
