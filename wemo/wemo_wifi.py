import os, time, sys
# connect to wemo device wifi; Note: wemo Netcam does not have wemo in wifi name
def connect_wemo_wifi(netcam_mode=False):
    p = os.popen('airport -s', 'r')
    print 'Searching for WeMo networks..', # <string>, format required to remove \n
    for line in p:
        print '.', # <string>, format required to remove \n
        sys.stdout.flush()
        time.sleep(0.1)
        if ('netcam' if netcam_mode else 'wemo') in line.lower():
            k = 0
            while k + 2 < len(line):
                if line[k] == ' ' and line[k + 1] == ' ':
                    line = line[:k] + line[k + 1:]
                else:
                    k += 1
            fields = line.split(' ')
            name = fields[1]
            mac = fields[2]
            strength = fields[3]
            security = fields[7]
            print("\nFound WEMO device:\n\tName: " + name + "\n\tMAC: " + mac + "\n\tRSSI: " + strength + "\n\tSecurity: " + security)
            x = raw_input("Would you like connect to this device's Wifi to communciate with it? (Y/N)")
            if "y" in x.lower():
                p2 = os.popen('networksetup -setairportnetwork en1 ' + name)
                print "Connecting to the " + name + " wifi network.", # <string>, format required to remove \n
                for k in range(0,15):
                    print '.', # <string>, format required to remove \n
                    sys.stdout.flush()
                    time.sleep(0.5)
                print('done.')
                return
            else:
                print 'Continuing search.', # <string>, format required to remove \n
# if run from terminal, call function
if __name__ == '__main__':
    connect_wemo_wifi()
