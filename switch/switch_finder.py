import os, time, sys, switch

def comm(name):
	print "Connecting to the " + name + " wifi network.",
	for k in range(0,15):
		print ".",
		sys.stdout.flush()
		time.sleep(0.5)
	print("\n")
	binary_device = wemo_binary.wemo_binary()
	print(binary_device)
	r = ""
	print('Type get, set [state], or quit')
	while not 'q' in r.lower():
		r = raw_input() # PYTHON 2
		if 'get' in r.lower():
			print(binary_device)
		elif 'set' in r.lower():
			new_state = r.split(' ')[1]
			binary_device.setState(new_state.lower() == 'on' or new_state == '1')
			print(binary_device)

p = os.popen('airport -s', 'r')
for line in p:
	if 'wemo' in line.lower():
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
		print("Found WEMO device:\n\tName: " + name + "\n\tMAC: " + mac + "\n\tRSSI: " + strength + "\n\tSecurity: " + security)
		x = raw_input("Would you like connect to this device's Wifi to communciate with it? (Y/N)")
		if "y" in x.lower():
			p2 = os.popen("networksetup -setairportnetwork en1 Wemo.Mini.BEE")
			comm(name)
