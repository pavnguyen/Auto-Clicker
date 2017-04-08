import sys


if len(sys.argv) > 3:
    debut = int(sys.argv[1])
    fin = int(sys.argv[2])
    ossys = sys.argv[3]
else:
    print('Please put the First Machine: ')
    debut = int(raw_input())
    print('Please put the Last Machine: ')
    fin = int(raw_input())
    print('[L]inux/[W]indows: ')
    ossys = raw_input()

a = open('Autorun_Windows.bat', 'w+')

if ossys == 'w' or ossys == 'W':
    ajout = ""
    c = open('Create Clone Linked VMware.bat', 'w+')
    s = open('Start_Windows.bat', 'w+')

if ossys == 'l' or ossys == 'L':
    ajout = 'L'
    c = open('Create Clone Linked VMware LINUX.bat', 'w+')
    s = open('Start_Linux.bat', 'w+')


for i in range(debut, fin + 1):
    try:

        cmd = 'vmrun -gu cas -gp cas runProgramInGuest ' + '\"E:/Virtual Machine/'+ str(i) + \
        '/' + str(i) + '.vmx\"' + ' -activeWindow -interactive -nowait ' + \
        '\"Z:/Project Python/Auto-Clicker/ressources/Batch_Files/AC.bat\" ' + str(i)

        cmd_delete = 'vmrun deleteVM ' + '\"E:/Virtual Machine/' + ajout + str(i) + '/' + str(i) + '.vmx\"'

        cmd_clone = 'vmrun clone ' + '\"E:/Virtual Machine/May Ao Chuan/Windows 7 x64.vmx\" ' + \
        '\"E:/Virtual Machine/' + ajout + str(i) + '/' + str(i) + '.vmx\" ' + 'linked -cloneName=\"' + str(i) + '\"'

        cmd_start = 'vmrun start ' + '\"E:/Virtual Machine/' + ajout + str(i) + '/' + str(i) + '.vmx\"'

        a.write(cmd + '\n')
        c.write(cmd_delete + '\n' + cmd_clone + '\n')
        s.write(cmd_start + '\n')
    except:
        print('Error')
        continue
a.close()
c.close()
s.close()
