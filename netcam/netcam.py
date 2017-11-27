import requests
from requests.auth import HTTPBasicAuth
# get netcam data
def getNetcam(path, file_output=None, debug=False):
    # have not tested which headers are required, currently using exact headers from correct usage
    response = requests.get('http://10.68.68.22:80/' + path, auth=HTTPBasicAuth('admin', 'admin'))
    if file_output == None:
        # print content to terminal
        print('Data:\n' + response.content + '\n')
    else:
        # output content to file
        try:
            f = open(file_output, 'w+')
            f.write(response.content)
            f.close()
        except Exception as e:
            print("Output error: ", e.message)
    # debug - respnse headers
    if debug:
        print('Status: ' + str(response.status_code))
        for key in response.headers.keys():
            print(key + ": " + response.headers[key])
        print('\n')
# post netcam data
def postNetcam(path, debug, data_dict):
    response = requests.post('http://10.68.68.22:80/' + path, data=data_dict, auth=HTTPBasicAuth('admin', 'admin'), headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive', 'Accept-Lanuage':'en-US', 'Accept-Encoding':'gzip, deflate', 'Referer':'http://10.68.68.22/apcam/for-android/CamPreview.asp?SeedonkServerIp=server.seedonk.com&PartnerId=Belkin&TZ=America/Detroit&LanguageId=0', 'Accept':'image/webp,image/apng,image/*,*/*;q=0.8', 'X-Requested-With':'com.belkin.android.androidbelkinnetcam'})
    # debug - respnse headers
    if debug:
        print('Status: ' + str(response.status_code))
        for key in response.headers.keys():
            print(key + ": " + response.headers[key])
        print('\n')
# sample usage
print('. . . GET . . .')
#getNetcam('goform/getSystemSettings?cameraname', None, True)
print('. . . POST . . .')
#postNetcam('goform/getSystemSettings/', True, {'cameraname':'TestCameraName'})
