from os import listdir

for onlyFilesVPN in listdir('ressources\config'):
    if "vpn" in onlyFilesVPN:
        with open('ressources\config\\' + onlyFilesVPN) as input:
            # Read non-empty lines from input file
            lines = [line for line in input if line.strip()]
        with open('ressources\config\\' + onlyFilesVPN, "w") as output:
            for line in lines:
                if "auth-user-pass" in line:
                    output.write('auth-user-pass auth.txt\n')
                else:
                    output.write(line)
