import hashlib
import os
import random
import sys

try:
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = 'videos/'
    dirs = os.listdir(path)
except:
    print('Error Folder!!!')
    pass

try:
    for file_source in dirs:
        print('[File to change MD5]  ' + file_source)
        old_md5 = hashlib.md5(open(path + file_source, 'rb').read()).hexdigest() \
 \
        file_opened = open(path + file_source, 'rb').read()
        with open(path + file_source, 'wb') as new_file:
            value_random = random.randint(1, 99) * random.randint(1, 99)
            new_file.write(file_opened + '\0' * value_random)  # add a null to change the file content

        new_md5 = hashlib.md5(open(path + file_source, 'rb').read()).hexdigest()
        print(' ' * 22 + '[Old MD5] ' + old_md5 + ' ---> [New MD5] ' + new_md5)
    print('DONE! DONE! DONE!')
except:
    print('Error: change MD5 failed!')
    pass
