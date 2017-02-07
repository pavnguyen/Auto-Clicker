import hashlib
import os
import random
import sys


def get_name_channel(number):
    try:
        name = LIST_CHANNEL.get(number)
    except:
        name = ''
    return name


LIST_CHANNEL = {
    1: '[MCC]'
    , 2: '[JAY]'
    , 3: '[HAR]'
    , 4: '[BRO]'
    , 5: '[JOR]'
    , 6: '[WIL]'
    , 7: '[ELI]'
    , 8: '[BUY]'
    , 9: '[JM5]'
    , 10: '[TRO]'
    , 11: '[BEA]'
    , 12: '[JOP]'
}

try:
    if len(sys.argv) > 1:
        NBR_CHANNEL = int(sys.argv[1])
    else:
        print('Enter number of channel to create: ')
        NBR_CHANNEL = int(raw_input())

    path = 'videos/'
    dirs = os.listdir(path)
except:
    print('Error Folder!!!')
    pass

list_files = []
for file in dirs:
    list_files.append(file)

try:
    for file in list_files:
        for i in range(0, NBR_CHANNEL):
            value_random = random.randint(1, 99) * random.randint(1, 99)
            if i == 0:
                file_source = path + file
            else:
                file_source = path + get_name_channel(i) + ' ' + file

            print('[File to change MD5]  ' + file_source)

            old_md5 = hashlib.md5(open(file_source, 'rb').read()).hexdigest()
            file_opened = open(file_source, 'rb').read()

            i += 1
            with open(path + get_name_channel(i) + ' ' + file, 'wb') as new_file:
                new_file.write(file_opened + '\0' * value_random)  # add a null to change the file content

            new_md5 = hashlib.md5(open(path + get_name_channel(i) + ' ' + file, 'rb').read()).hexdigest()
            print(' ' * 22 + '[Old MD5] ' + old_md5 + ' ---> [New MD5] ' + new_md5)
    print('DONE! DONE! DONE!')
except:
    print('Error: change MD5 failed!')
    pass
