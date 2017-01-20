import hashlib
import os
import random
import sys


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

try:
    for file in dirs:
        for i in range(0, NBR_CHANNEL):
            value_random = random.randint(1, 99) * random.randint(1, 99)
            if i == 0:
                file_source = path + file
            else:
                file_source = path + str(i) + '_' + file

            print('[File to change MD5]  ' + file_source)

            old_md5 = hashlib.md5(open(file_source, 'rb').read()).hexdigest()
            file_opened = open(file_source, 'rb').read()

            i += 1
            with open(path + str(i) + '_' + file, 'wb') as new_file:
                new_file.write(file_opened + '\0' * value_random)  # add a null to change the file content

            new_md5 = hashlib.md5(open(path + str(i) + '_' + file, 'rb').read()).hexdigest()
            print(' ' * 22 + '[Old MD5] ' + old_md5 + ' ---> [New MD5] ' + new_md5)
    print('DONE! DONE! DONE!')
except:
    print('Error: change MD5 failed!')
    pass
