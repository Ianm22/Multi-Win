from typing import Text
from Model.model import *
from pathlib import Path
import re
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Variables

selected_apps = {
    'app1': None,
    'app2': None,
    'app3': None,
    'app4': None
}

home = str(Path.home())

config_dir_config = "/.config/multi-win/config/"
config_dir_scripts = "/.config/multi-win/scripts/"
config_dir_quick_access =  "/.local/share/applications/"

# re.sub () is for if I implement a configuration window and a user wants to change their path
dir_config = os.path.dirname(home + re.sub("/home/[A-Za-z]/", "",config_dir_config))
dir_scripts = os.path.dirname(home + re.sub("/home/[A-Za-z]/", "",config_dir_scripts))
dir_quick_access = os.path.dirname(home + re.sub("/home/[A-Za-z]/", "",config_dir_quick_access))

# Think later if is a good idea left this or not
class Controls:

    def __init__(self, builder_in):
        self.builder = builder_in

    def showRemoveAppList(self):
        for label in self.builder.get_object('listBox_removeApp'):
            self.builder.get_object('listBox_removeApp').remove(label)
        
        data = getAppsList(dir_config)
        for app in data:
            self.builder.get_object('listBox_removeApp').add((Gtk.Label(label=app)))
        
        self.builder.get_object('listBox_removeApp').show_all()

    def clearAll(self):
        self.builder.get_object('lbl_newAppName').set_text('')
        
        for app in selected_apps:
            selected_apps[app] = None

        print(selected_apps)
        self.showRemoveAppList()

class Signals:

    def __init__(self, builder_in):
        self.builder = builder_in
        self.controls = Controls(builder_in)

    def getAppChooserDialog(self, *arg, label=str):
        
        def on_response(dialog, response):
            if response == Gtk.ResponseType.OK:
                app_info = dialog.get_app_info()
                
                if label == 'Select App 1':
                    selected_apps['app1'] = app_info.get_commandline()
                    self.builder.get_object('lbl_app_1').set_label(app_info.get_display_name())
                elif label == 'Select App 2':
                    self.builder.get_object('lbl_app_2').set_label(app_info.get_display_name())
                    selected_apps['app2'] = app_info.get_commandline()
                elif label == 'Select App 3':
                    self.builder.get_object('lbl_app_3').set_label(app_info.get_display_name())
                    selected_apps['app3'] = app_info.get_commandline()
                elif label == 'Select App 4':
                    self.builder.get_object('lbl_app_4').set_label(app_info.get_display_name())
                    selected_apps['app4'] = app_info.get_commandline()
                
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
        selected_apps['app3'] = None
        selected_apps['app4'] = None

    def select_3(self, radiobutton):
        self.builder.get_object('app_box_3').show()
        self.builder.get_object('app_box_4').hide()
        self.builder.get_object('lbl_app_4').set_label('App 4')
        selected_apps['app4'] = None

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


    def row_selected(self, listbox, row):
        self.removeAppRow = row


    def createApp_btn(self, button):
        lbl_text = self.builder.get_object('lbl_newAppName').get_text()
        if lbl_text != '':
            new_app_name = self.builder.get_object('lbl_newAppName').get_text()
            
            output_script = create_script(new_app_name, selected_apps, dir_scripts)

            if output_script:
                output_QA = create_quick_access(new_app_name, dir_quick_access, dir_scripts)

            if output_script and output_QA:
                self.builder.get_object('lbl_output').set_text('All ok!')
                addAppIntoList(dir_config, new_app_name, dir_quick_access, dir_scripts)
                # Clear appList, lbl_newAppName and refresh remove list
                self.controls.clearAll()
            else:
                self.builder.get_object('lbl_output').set_text('Something went wrong at the app creation!')
        else:
            self.builder.get_object('lbl_output').set_text('Insert a name for the app!')


    def removeApp_btn(self, button):
        name_quick_access = self.removeAppRow.get_child().get_text()
        removeApp(dir_config, name_quick_access)
        
        self.controls.showRemoveAppList()
        

        


