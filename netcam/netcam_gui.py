import gi, requests, thread, ../wemo/wemo_wifi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="NetCam Preview")
        self.image = Gtk.Image()
        self.image.set_from_file("newest_image.jpeg")
        self.image.show()
        self.add(self.image)
    # stream video data via mjpeg
    def stream(self):
        s = requests.session()
        stream = s.get('http://admin:admin@10.68.68.22:80/goform/video', stream=True)
        if stream.ok:
            # get header; stream, so this loops until stream or app closes
            for chunk in stream.iter_content(chunk_size=77):
                if not m_running and stream.ok:
                    break
                # get jpeg data
                size = int(chunk[-10:-4])
                for image_data in stream.iter_content(chunk_size=size + 2):
                    loader = GdkPixbuf.PixbufLoader()
                    loader.write(image_data[:-2])
                    # set image
                    self.image.set_from_pixbuf(loader.get_pixbuf())
                    loader.close()
                    break

wemo_wifi.connect_wemo_wifi(True)
m_running = True
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
# stream data on thread separate from gui thread
thread.start_new_thread(win.stream, ())
Gtk.main()
m_running = False
