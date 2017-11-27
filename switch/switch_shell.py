import wemo_binary, ../wemo/wemo_wifi.py

def switch_shell():
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
