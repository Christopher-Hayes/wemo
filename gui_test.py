import gi, requests, time
from gi.repository import GObject
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from requests.auth import HTTPBasicAuth

def getNetcam(num):
    print(num)
    response = requests.get('http://10.68.68.22:80/goform/snapshot?n=' + str(num), auth=HTTPBasicAuth('admin', 'admin'), headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive', 'Accept-Lanuage':'en-US', 'Accept-Encoding':'gzip, deflate', 'Referer':'http://10.68.68.22/apcam/for-android/CamPreview.asp?SeedonkServerIp=server.seedonk.com&PartnerId=Belkin&TZ=America/Detroit&LanguageId=0', 'Accept':'image/webp,image/apng,image/*,*/*;q=0.8', 'X-Requested-With':'com.belkin.android.androidbelkinnetcam'})
    f = open('newest_image.jpeg', 'w+')
    f.write(response.content)
    f.close()

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.hbox = Gtk.HBox()
        self.hbox.show()
        self.add(self.hbox)

        self.image = Gtk.Image()
        self.image.set_from_file("newest_image.jpeg")
        self.image.show()
        self.hbox.add(self.image)

        self.image2 = Gtk.Image()
        self.image2.set_from_file("newest_image.jpeg")
        self.image2.show()
        self.hbox.add(self.image2)

        self.image_counter = 1
        GObject.timeout_add(250, self.update_image);

    def update_image(self):
        getNetcam(self.image_counter)
        self.image_counter += 1
        self.image.set_from_file("newest_image.jpeg")
        self.image.show()

        getNetcam(1)
        self.image2.set_from_file("newest_image.jpeg")
        self.image2.show()

        return True

response = requests.get('http://10.68.68.22:80/goform/getSystemSettings?systemModel&systemVersion', headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive'})
print(response.status_code)
print(response.content)
response = requests.get('http://10.68.68.22:80/goform/getSystemSettings?systemModel&systemVersion', auth=HTTPBasicAuth('admin', 'admin'), headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive'})
print(response.status_code)
print(response.content)

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
