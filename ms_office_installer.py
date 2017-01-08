import os
import stat
import subprocess
# import getpass


class MSOfficeInstaller:
    def __init__(self, file_name):
        self.f_name = file_name

    def set_exec_permission(self):
        file_permissions = self.get_file_permissions()
        if not os.access(self.f_name, os.X_OK):
            os.chmod(self.f_name, file_permissions + stat.S_IXUSR)
        self.get_file_permissions()

    def get_file_permissions(self):
        f_permissions = stat.S_IMODE(os.stat(self.f_name).st_mode)
        print('file {name} current permissions is {permissions}'.format(name=self.f_name, permissions=oct(f_permissions)))
        return f_permissions

    def run_installer(self):
        prefix = 'wine32office'
        config_directory = '.'
        office_installer_name = '/media/open64/Data/Установки/office.2010.x86.iso'
        cmd = ['./%s' % self.f_name, '-p', prefix, '-o', office_installer_name, '-c', config_directory]
        # passwd = self.getpass()
        p = subprocess.run(cmd, stdout=subprocess.PIPE)
        print(p.args)
        print(p.stdout.decode())

    # this no need already but I leave this here as example
    @staticmethod
    def getpass(prompt="Password: "):
        import termios
        import sys
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO          # lflags
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, new)
            passwd = input(prompt)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            print()
        return passwd


installer_file_name = 'installer.sh'

if os.access(installer_file_name, os.F_OK):
    office_installer = MSOfficeInstaller(installer_file_name)
    office_installer.set_exec_permission()
    office_installer.run_installer()
else:
    print('No installer file.\nPlease check installer.sh file.')

