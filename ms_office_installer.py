import os
import stat
import re


__version__ = '0.2.0'
__author__ = 'Yurii Zhytskyi'


class MSOfficeInstaller:
    def __init__(self, file_name):
        self.f_name = file_name
        self.desktop_files = dict()
        self.programs = dict()
        self.wine_prefixes = dict()
        self.programs_path = dict()
        self.share_folder = '%s/.local/share/' % os.environ['HOME']

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
        import sys
        cmd = ['./%s' % self.f_name] + sys.argv[1:]
        os.system(' '.join(cmd))

    def fix_application_list(self):
        curr_path = os.getcwd()
        os.chdir('%s/.local/share/applications' % os.environ['HOME'])
        self._parse_desktop_file()
        self._get_desktop_file_for_each_program()
        self._get_progid_for_each_wineprefix()
        self._find_programs_path_by_progid()
        self._create_new_desktop_files()
        self._remove_old_desktop_files()
        self._update_desktop_and_mime_databases()
        os.chdir(curr_path)

    def _update_desktop_and_mime_databases(self):
        os.system('update-desktop-database %s/applications' % self.share_folder)
        os.system('update-mime-database %s/mime' % self.share_folder)

    def _remove_old_desktop_files(self):
        for old_desktop_file in self.desktop_files:
            os.remove(old_desktop_file)

    def _create_new_desktop_files(self):
        for prog in self.programs:
            with open('%s.desktop' % prog, 'w') as new_desktop_file:
                new_desktop_file.write('[Desktop Entry]\n')
                curr_prog = self.desktop_files[self.programs[prog][0]]
                key_names = ('Type', 'Name', 'Icon', 'NoDisplay', 'StartupNotify')
                for key in key_names:
                    if key in curr_prog:
                        new_desktop_file.write('%s=%s\n' % (key, curr_prog[key]))
                new_desktop_file.write(
                    '%s=%s\n' % ('Exec', curr_prog['Exec']['Command'].format(
                        path=self.programs_path[curr_prog['Exec']['ProgIDOpen']]))
                )
                new_desktop_file.write(
                    '%s=%s\n' % ('MimeType', ''.join([self.desktop_files[p]['MimeType'] for p in self.programs[prog]])))

    def _find_programs_path_by_progid(self):
        for prefix in self.wine_prefixes:
            with open('%s/system.reg' % prefix) as reg:
                reg_file = reg.read()
                for id_ in self.wine_prefixes[prefix]:
                    founded_path = re.search(r'\[Software\\\\Classes\\\\' + '\\.'.join(id_.split('.')) +
                                             r'\\\\shell\\\\Open\\\\command\]' +
                                             '((.+\n)+)@=\"(\\\\\")?([^\"]+)\\\\?\"', reg_file, re.IGNORECASE)
                    if founded_path:
                        self.programs_path[id_] = founded_path.groups()[-1].strip(' %1').strip('\\\\')

    def _get_progid_for_each_wineprefix(self):
        for desktop in self.desktop_files:
            exec_ = self.desktop_files[desktop]['Exec'].split(' ')
            prog_id_ind = exec_.index('/ProgIDOpen')
            for i in exec_:
                matched = re.match('WINEPREFIX=\\"(.+)\\"', i)
                if matched:
                    self.wine_prefixes.setdefault(matched.group(1), set()).add(exec_[prog_id_ind + 1])
            self.desktop_files[desktop]['Exec'] = {
                'Command': ' '.join(exec_[:prog_id_ind]) + ' {path} ' + exec_[-1],
                'ProgIDOpen': exec_[prog_id_ind + 1]
            }

    def _get_desktop_file_for_each_program(self):
        for desktop in self.desktop_files:
            self.programs.setdefault(self.desktop_files[desktop]['Name'], []).append(desktop)

    def _parse_desktop_file(self):
        import glob
        mime_type_list = glob.glob('wine-extension-*.desktop')
        for mime in mime_type_list:
            with open(mime) as mime_file:
                self.desktop_files[mime] = dict()
                for line in mime_file:
                    striped_line = line.strip()
                    if striped_line and striped_line[0] != '[' and striped_line[-1] != ']':
                        key, value = striped_line[:striped_line.find('=')], striped_line[striped_line.find('=') + 1:]
                        self.desktop_files[mime][key] = value

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
    office_installer.fix_application_list()
else:
    print('No installer file.\nPlease check installer.sh file.')
