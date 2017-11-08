import requests
from requests.auth import HTTPBasicAuth

"""
Netcam App Network Sequence - Screenshot Preview:
 - send anonymous analytic data to server
 - get system settings from Belkin device
 - get js display code to show screenshot preview
 - continuously get snapshots for the preview
    - preview updates by incrementing an integer, new int = take snapshot, old int = send old snapshot
# old ip: http://10.68.68.22:80/
# Online camera - Web of Trust
"""

def getNetcam(path, name, header_auth):
    if header_auth:
        response = requests.get('http://10.2.11.45:9490/' + path, auth=HTTPBasicAuth('admin', 'admin'), headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive', 'Accept-Lanuage':'en-US', 'Accept-Encoding':'gzip, deflate', 'Referer':'http://10.68.68.22/apcam/for-android/CamPreview.asp?SeedonkServerIp=server.seedonk.com&PartnerId=Belkin&TZ=America/Detroit&LanguageId=0', 'Accept':'image/webp,image/apng,image/*,*/*;q=0.8', 'X-Requested-With':'com.belkin.android.androidbelkinnetcam'})
    else:
        response = requests.get('http://10.2.11.45:9490/' + path, headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive', 'Accept-Lanuage':'en-US', 'Accept-Encoding':'gzip, deflate', 'Referer':'http://10.68.68.22/apcam/for-android/CamPreview.asp?SeedonkServerIp=server.seedonk.com&PartnerId=Belkin&TZ=America/Detroit&LanguageId=0', 'Accept':'image/webp,image/apng,image/*,*/*;q=0.8', 'X-Requested-With':'com.belkin.android.androidbelkinnetcam'})
    print(response.status_code)
    f = open(name, 'w+')
    f.write(response.content)
    f.close()
    for key in response.headers.keys():
        print(key + ": " + response.headers[key])

getNetcam('goform/snapshot?n=28', 'snap4.jpeg', True)
