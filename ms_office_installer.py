import os
import stat
import time
import re


__version__ = '0.1.1'
__author__ = 'Yurii Zhytskyi'


class MSOfficeInstaller:
    def __init__(self, file_name):
        self.f_name = file_name
        self.prefix = 'wine32office2'

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
        config_directory = '.'
        office_installer_name = '/media/open64/Data/Установки/office.2010.x86.iso'
        cmd = ['./%s' % self.f_name, '-p', self.prefix, '-o', office_installer_name, '-c', config_directory, '-v', '-b']
        os.system(' '.join(cmd))

    def fix_application_list(self):
        a1 = time.clock()
        import glob
        curr_path = os.getcwd()
        os.chdir('%s/.local/share/applications' % os.environ['HOME'])
        programs = dict()
        desktop_files = dict()
        mime_type_list = glob.glob('wine-extension-*.desktop')
        for mime in mime_type_list:
            with open(mime) as mime_file:
                desktop_files[mime] = dict()
                for line in mime_file:
                    striped_line = line.strip()
                    if striped_line and striped_line[0] != '[' and striped_line[-1] != ']':
                        key, value = striped_line[:striped_line.find('=')], striped_line[striped_line.find('=')+1:]
                        desktop_files[mime][key] = value
        for desktop in desktop_files:
            programs.setdefault(desktop_files[desktop]['Name'], []).append(desktop)
        wine_prefixes = dict()
        for desktop in desktop_files:
            exec_ = desktop_files[desktop]['Exec'].split(' ')
            prog_id_ind = exec_.index('/ProgIDOpen')
            for i in exec_:
                matched = re.match('WINEPREFIX=\\"(.+)\\"', i)
                if matched:
                    wine_prefixes.setdefault(matched.group(1), set()).add(exec_[prog_id_ind + 1])
            desktop_files[desktop]['Exec'] = {
                'Command': ' '.join(exec_[:prog_id_ind]) + ' {path} ' + exec_[-1],
                'ProgIDOpen': exec_[prog_id_ind + 1]
            }
        path = dict()
        print(time.clock() - a1)
        for prefix in wine_prefixes:
            with open('%s/system.reg' % prefix) as reg:
                reg_file = reg.read()
                for id_ in wine_prefixes[prefix]:
                    founded_path = re.search(r'\[Software\\\\Classes\\\\' + '\\.'.join(id_.split('.')) +
                                             r'\\\\shell\\\\Open\\\\command\]' +
                                             '((.+\n)+)@=\"(\\\\\")?([^\"]+)\\\\?\"', reg_file, re.IGNORECASE)
                    if founded_path:
                        path[id_] = founded_path.groups()[-1].strip(' %1').strip('\\\\')
        for prog in programs:
            with open('%s.desktop' % prog, 'w') as new_desktop_file:
                new_desktop_file.write('[Desktop Entry]\n')
                curr_prog = desktop_files[programs[prog][0]]
                key_names = ('Type', 'Name', 'Icon', 'NoDisplay', 'StartupNotify')
                for key in key_names:
                    if key in curr_prog:
                        new_desktop_file.write('%s=%s\n' % (key, curr_prog[key]))
                new_desktop_file.write(
                    '%s=%s\n' % ('Exec', curr_prog['Exec']['Command'].format(path=path[curr_prog['Exec']['ProgIDOpen']]))
                )
                new_desktop_file.write('%s=%s\n' % ('MimeType', ''.join([desktop_files[p]['MimeType'] for p in programs[prog]])))
        for old_desktop_file in desktop_files:
            os.remove(old_desktop_file)
        os.system('update-desktop-database %s/.local/share/applications' % os.environ['HOME'])
        os.system('update-mime-database %s/.local/share/mime' % os.environ['HOME'])
        os.chdir(curr_path)

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
    # office_installer.set_exec_permission()
    # office_installer.run_installer()
    office_installer.fix_application_list()
else:
    print('No installer file.\nPlease check installer.sh file.')
