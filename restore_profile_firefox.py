import getpass
import os
import zipfile


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)


userName = getpass.getuser()
path = 'C:\Users\\' + userName + '\AppData\Roaming\Mozilla\Firefox\Profiles\\'
profilName = os.listdir(path)[0]
path += profilName

print('Please put the machine\'s number:')
numberMachine = str(raw_input())

unzip('Z:\M Chien\Profile Firefox\\' + numberMachine + '.zip', path)
print('Profil Firefox is restored!!!')
