from model import *
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

arrayApps = [None,None,None,None]
dir_scripts = os.path.dirname("/home/paul/.config/multi-win/") 
dir_quick_access = os.path.dirname("/home/paul/.local/share/applications/")

class Handler:

    def __init__(self, builder_in):
        self.builder = builder_in

    def getAppChooserDialog(self, *arg, label=str):
        print(arrayApps)
        
        def on_response(dialog, response):
            if response == Gtk.ResponseType.OK:
                app_info = dialog.get_app_info()
                
                if label == 'Select App 1':
                    arrayApps[0] = app_info.get_commandline()
                    self.builder.get_object('lbl_app_1').set_label(app_info.get_display_name())
                elif label == 'Select App 2':
                    self.builder.get_object('lbl_app_2').set_label(app_info.get_display_name())
                    arrayApps[1] = app_info.get_commandline()
                elif label == 'Select App 3':
                    self.builder.get_object('lbl_app_3').set_label(app_info.get_display_name())
                    arrayApps[2] = app_info.get_commandline()
                elif label == 'Select App 4':
                    self.builder.get_object('lbl_app_4').set_label(app_info.get_display_name())
                    arrayApps[3] = app_info.get_commandline()
                
            dialog.destroy()

        app_chooser_1 = Gtk.AppChooserDialog()
        app_chooser_1.set_heading("Select an app")

        widget = app_chooser_1.get_widget()
        widget.set_show_all(True)

        app_chooser_1.connect("response", on_response)
        app_chooser_1.show()
        

    def onDestroy(self, *args):
        Gtk.main_quit()

    def select_2(self, radiobutton):
        self.builder.get_object('app_box_3').hide()
        self.builder.get_object('app_box_4').hide()
        self.builder.get_object('lbl_app_3').set_label('App 3')
        self.builder.get_object('lbl_app_4').set_label('App 4')
        arrayApps[2] = None
        arrayApps[3] = None


    def select_3(self, radiobutton):
        self.builder.get_object('app_box_3').show()
        self.builder.get_object('app_box_4').hide()
        self.builder.get_object('lbl_app_4').set_label('App 4')
        arrayApps[3] = None 

    def select_4(self, radiobutton):
        self.builder.get_object('app_box_3').show() 
        self.builder.get_object('app_box_4').show()
    
    

    def app_btn_1(self, widget):
        print(widget.get_label())
        self.getAppChooserDialog(label=widget.get_label())

    def app_btn_2(self, widget):
        print(widget.get_label())
        self.getAppChooserDialog(label=widget.get_label())

    def app_btn_3(self, widget):
        print(widget.get_label())
        self.getAppChooserDialog(label=widget.get_label())
        
    def app_btn_4(self, widget):
        print(widget.get_label())
        self.getAppChooserDialog(label=widget.get_label())

    def createApp_btn(self, button):
        new_app_name = self.builder.get_object('lbl_newAppName').get_text()
        
        create_script(new_app_name, arrayApps, dir_scripts)
        create_quick_access(new_app_name, dir_quick_access, dir_scripts, arrayApps)

