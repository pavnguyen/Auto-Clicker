import getpass
import os
import zipfile


class BackupProfileFirefox:
    def zip(self, src, dst):
        zf = zipfile.ZipFile('%s.zip' % (dst), 'w', zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(src)
        for dirname, subdirs, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                print('zipping %s as %s' % (os.path.join(dirname, filename),
                                            arcname))
                zf.write(absname, arcname)
        zf.close()

    def backup_profile(self, numberMachine):
        userName = getpass.getuser()
        path = 'C:\Users\\' + userName + '\AppData\Roaming\Mozilla\Firefox\Profiles\\'
        profilName = os.listdir(path)[0]
        path += profilName
        self.zip(path, 'Z:\M Chien\Profile Firefox\\' + str(numberMachine))
        print('Profil Firefox is backup!!!')
