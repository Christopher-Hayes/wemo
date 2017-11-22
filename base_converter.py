import base64

a = input('Base64: ')
print('UTF-8:', base64.b64decode(a).decode('UTF-8'))
