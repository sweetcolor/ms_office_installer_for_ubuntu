# Installer Microsoft Office for ubuntu
Installer microsoft office on ubuntu using wine.
Only for MS Office 2010

## Overview

After installing any Windows program on Ubuntu using wine 
there is problem with mime types and application list in context menu of Nautilus.
Wine create *.desktop files for each new MIME type and many of them linked to 
same program path.
So this projects started as simple script for installing MS Office and merge all MIME types
and create merged *.desktop file for each program, not for only one MIME type.

## Installing

just download source code

## Using

First run installer.sh for installing wine and ms office.

    $ ./installer.sh -o <path to office installer> -p <new wineprefix name> -v <wine version>
    
Next you need run ms_office_installer.py file for fixing mime types in *.desktop files which will created by wine
 
    $ python3 ms_office_installer.py

## Parameters
#### -o, --office-installer

Path to MS Office installer. Installer can be *.exe or *.iso file  

#### -p, --prefix

Name of new WINEPREFIX where will be installed MS Office

#### -v, --version

Wine version what will be installed for MS Office. You can choose any version what you want.

    -v 1.9

If you need latest version (build version), just write flag _-b_ or _--build_

    -v --build

## Examples

    $ ./installer.sh -o /home/user/office.iso -p wine32office -v 1.9
    $ python3 ms_office_installer.py

## Version

Version 0.2.0

Current program status: in develop. 

## License

BSD v3 License