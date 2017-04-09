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

if ossys == 'w' or ossys == 'W':
    ajout = ''
    c = open('Create Clone Linked Windows.bat', 'w+')
    s = open('Start_Windows.bat', 'w+')
    a = open('Autorun_Windows.bat', 'w+')

if ossys == 'l' or ossys == 'L':
    ajout = 'L'
    c = open('Create Clone Linked Linux.bat', 'w+')
    s = open('Start_Linux.bat', 'w+')
    a = open('Autorun_Linux.bat', 'w+')


for i in range(debut, fin + 1):
    try:
        if ossys == 'w' or ossys == "W":
            cmd = 'vmrun -gu cas -gp cas runProgramInGuest ' + '\"E:/Virtual Machine/'+ str(i) + \
            '/' + str(i) + '.vmx\" -activeWindow -interactive -nowait ' + \
            '\"Z:/Project Python/Auto-Clicker/ressources/Batch_Files/AC.bat\" ' + str(i)
        else:
            cmd = 'vmrun -T ws -gu linux -gp linux runProgramInGuest ' +\
                  '\"E:/Virtual Machine/L' + str(i) + '/' + str(i) + '.vmx\" -activewindow -interactive -nowait ' + \
                  '\"/usr/bin/sakura\" \"-x\" \"/bin/bash /home/linux/AC.sh 1\"'
        print(cmd)

        cmd_delete = 'vmrun deleteVM ' + '\"E:/Virtual Machine/' + ajout + str(i) + '/' + str(i) + '.vmx\"'
        print(cmd_delete)
        
        if ossys == 'w' or ossys == "W":
            cmd_clone = 'vmrun clone ' + '\"E:/Virtual Machine/May Ao Chuan/Windows 7 x64.vmx\" ' + \
            '\"E:/Virtual Machine/' + ajout + str(i) + '/' + str(i) + '.vmx\" ' + 'linked -cloneName=\"' + str(i) + '\"'
        else:
            cmd_clone = 'vmrun clone ' + '\"E:/Virtual Machine/Ubuntu/Ubuntu.vmx\" ' + \
            '\"E:/Virtual Machine/' + ajout + str(i) + '/' + str(i) + '.vmx\" ' + 'linked -cloneName=\"' + str(i) + '\"'
        print(cmd_clone)

        cmd_start = 'vmrun start ' + '\"E:/Virtual Machine/' + ajout + str(i) + '/' + str(i) + '.vmx\"'
        print(cmd_start)

        a.write(cmd + '\n')
        c.write(cmd_delete + '\n' + cmd_clone + '\n')
        s.write(cmd_start + '\n')
    except:
        print('Error')
        continue
a.close()
c.close()
s.close()
