import gi, requests, time, socket, thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from requests.auth import HTTPBasicAuth

def getNetcam(num):
    print(num)
    response = requests.get('http://10.68.68.22:80/goform/snapshot?n=' + str(num), auth=HTTPBasicAuth('admin', 'admin'), headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive', 'Accept-Lanuage':'en-US', 'Accept-Encoding':'gzip, deflate', 'Referer':'http://10.68.68.22/apcam/for-android/CamPreview.asp?SeedonkServerIp=server.seedonk.com&PartnerId=Belkin&TZ=America/Detroit&LanguageId=0', 'Accept':'image/webp,image/apng,image/*,*/*;q=0.8', 'X-Requested-With':'com.belkin.android.androidbelkinnetcam'})
    f = open('newest_image.jpeg', 'w+')
    f.write(response.content)
    f.close()

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="NetCam Preview")

        self.hbox = Gtk.HBox()
        self.hbox.show()
        self.add(self.hbox)

        self.image = Gtk.Image()
        self.image.set_from_file("newest_image.jpeg")
        self.image.show()
        self.hbox.add(self.image)

        #self.image2 = Gtk.Image()
        #self.image2.set_from_file("newest_image.jpeg")
        #self.image2.show()
        #self.hbox.add(self.image2)

        #self.image_counter = 1
        #GObject.timeout_add(250, self.update_image);

    def update_image(self):
        #getNetcam(self.image_counter)
        #self.image_counter += 1
        self.image.set_from_file("newest_image.jpg")
        self.image.show()

        #getNetcam(1)
        #self.image2.set_from_file("newest_image.jpeg")
        #self.image2.show()

        return True

    def stream(self):
        s = requests.session()
        stream = s.get('http://admin:admin@10.68.68.22:80/goform/video', stream=True)
        if stream.ok:
            x = True
            # get header
            for chunk in stream.iter_content(chunk_size=77):
                # get jpeg data
                size = int(chunk[-10:-4])
                print(size)
                snap = open('newest_image.jpg', 'wb')
                for image_data in stream.iter_content(chunk_size=size + 2):
                    snap.write(image_data[:-2])
                    loader = Gdk.PixbufLoader('jpeg')
                    loader.write(image_data[:-2])
                    loader.close()
                    # load pixbuf
                    pixbuf = loader.get_pixbuf()
                    # set image
                    gtk_image_set_from_pixbuf(self.image, pixbuf)
                    break
                snap.close()
                x = False


#response = requests.get('http://10.68.68.22:80/goform/getSystemSettings?systemModel&systemVersion', headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive'})
##print(response.content)
response = requests.get('http://admin:admin@10.68.68.22:80/goform/getSystemSettings?systemModel&systemVersion', headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)', 'Connection':'Keep-Alive'})
print(response.status_code)
print(response.content)
#response = requests.post('http://admin:admin@10.68.68.22:80/goform/video', headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N910V Build/MMB29M)'})
#print(response.status_code)
#print(response.content)

print("launch gtk")
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
thread.start_new_thread(win.stream, ())
Gtk.main()
