import random
import sys
import uuid


def randomMAC():
    return [0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]


def MACprettyprint(mac):
    return ':'.join(map(lambda x: "%02x" % x, mac))


def generate_mac():
    return str(MACprettyprint(randomMAC()))


def generate_uuid():
    # Make UUID
    new_uuid = str(uuid.uuid1())
    new_uuid = new_uuid.replace('-', '')
    new_uuid = ' '.join([new_uuid[i:i + 2] for i in range(0, len(new_uuid), 2)])
    new_uuid = new_uuid[:23] + '-' + new_uuid[24:]
    return new_uuid


def replace_uuid(path):
    lines = []
    with open(path) as infile:
        new_uuid = generate_uuid()
        for line in infile:
            if "uuid.bios = " in line:
                line = "uuid.bios = " + '\"' + new_uuid + '\"' + '\n'
            # if "uuid.location = " in line:
            #     line = "uuid.location = " + '\"' + new_uuid + '\"' + '\n'
            if "ethernet0.address = " in line:
                line = "ethernet0.address = " + '\"' + generate_mac() + '\"' + '\n'

            lines.append(line)
    with open(path, 'w') as outfile:
        for line in lines:
            outfile.write(line)


def change_uuid_mac_for(nbr_machine):
    path = 'E:\Virtual Machine\May Ao Chuan\Windows 7 x64.vmx'
    replace_uuid(path)

    for i in range(nbr_machine):
        number_machine = i + 1
        path = 'E:\Virtual Machine\\' + str(number_machine) + '\\' + str(number_machine) + '.vmx'
        replace_uuid(path)


# Change UUID for nbr_machine
if len(sys.argv) > 1:
    nbr_machine = int(sys.argv[1])
    print('Total machine: ' + str(nbr_machine))
else:
    print('Please put an argument!!!')

change_uuid_mac_for(nbr_machine)
