from Model.model import *
#from main import createAboutWindow
from pathlib import Path
import re
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# -----------------------------------------
# --------------- Variables ---------------
# -----------------------------------------
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

# -----------------------------------------
# --------------- Controls ----------------
# -----------------------------------------
class Controls:

    def __init__(self, builder_in):
        self.builder = builder_in

    # Create a new title bar
    def createTitleBar(self):
        window = self.builder.get_object("Main_window") 

        titlebar = self.builder.get_object("title_bar")
        window.set_titlebar(titlebar)

        menuitem_about = Gtk.MenuItem(label="About Multi-win")
        menuitem_about.connect("activate", self.show_about)
        menuitem_quite = Gtk.MenuItem(label="Quite")
        menuitem_quite.connect("activate", Gtk.main_quit)

        self.builder.get_object("menu_title").append(menuitem_about)
        self.builder.get_object("menu_title").append(menuitem_quite)
        self.builder.get_object("menu_title").show_all()

    # Show about dialog
    def show_about(self, *args):
        self.about_window = self.builder.get_object("About_window").run()

    # Show list of apps that user have combined
    def showRemoveAppList(self):
        for label in self.builder.get_object('listBox_removeApp'):
            self.builder.get_object('listBox_removeApp').remove(label)
        
        data = getAppsList(dir_config)
        for app in data:
            self.builder.get_object('listBox_removeApp').add((Gtk.Label(label=app)))
        
        self.builder.get_object('listBox_removeApp').show_all()

    # Clear all after combine apps
    def clearAll(self):
        self.builder.get_object('lbl_newAppName').set_text('')
        
        for app in selected_apps:
            selected_apps[app] = None
        
        for i in range(1,5):
            self.builder.get_object('lbl_app_{}'.format(i)).set_label('App {}'.format(i))

        self.showRemoveAppList()

    def getAppChooserDialog(self, *arg, label=str):
    # Temp function
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

        # Function starts here
        app_chooser_1 = Gtk.AppChooserDialog()
        app_chooser_1.set_heading("Select an app")

        widget = app_chooser_1.get_widget()
        widget.set_show_all(True)

        app_chooser_1.connect("response", on_response)
        app_chooser_1.show()
    
    
# -----------------------------------------
# ---------------- Signals ----------------
# -----------------------------------------
class Signals:

    def __init__(self, builder_in):
        self.builder = builder_in
        self.controls = Controls(builder_in)    


    # Close about dialog
    def hide_about(self, arg1, response):
        if response == -4:
            self.builder.get_object("About_window").hide()

    # When the window is destroyed, closes the application. 
    def onDestroy(self, *args):
        Gtk.main_quit()

    # Hide 3 and 4 'select app box'
    def main_window_show(self, *args):
        self.builder.get_object('app_box_3').hide()
        self.builder.get_object('app_box_4').hide()
        self.controls.showRemoveAppList()
        self.controls.createTitleBar()
        

    # When radioButton with number 2 is selected, hide '3' and '4' objects
    def select_2(self, radiobutton):
        self.builder.get_object('app_box_3').hide()
        self.builder.get_object('app_box_4').hide()
        self.builder.get_object('lbl_app_3').set_label('App 3')
        self.builder.get_object('lbl_app_4').set_label('App 4')
        selected_apps['app3'] = None
        selected_apps['app4'] = None

    # When radioButton with number 3 is selected, hide '4' objects and show '3' objects
    def select_3(self, radiobutton):
        self.builder.get_object('app_box_3').show()
        self.builder.get_object('app_box_4').hide()
        self.builder.get_object('lbl_app_4').set_label('App 4')
        selected_apps['app4'] = None

    # When radioButton with number 3 is selected, show all
    def select_4(self, radiobutton):
        self.builder.get_object('app_box_3').show() 
        self.builder.get_object('app_box_4').show()
    
    # Get application 1 and configure the label with the name of the selected application
    def app_btn_1(self, widget):
        self.controls.getAppChooserDialog(label=widget.get_label())

    # Get application 2 and configure the label with the name of the selected application
    def app_btn_2(self, widget):
        self.controls.getAppChooserDialog(label=widget.get_label())

    # Get application 3 and configure the label with the name of the selected application
    def app_btn_3(self, widget):
        self.controls.getAppChooserDialog(label=widget.get_label())
    
    # Get application 4 and configure the label with the name of the selected application
    def app_btn_4(self, widget):
        self.controls.getAppChooserDialog(label=widget.get_label())

    # If the row is selected, save the row in a variable
    def row_selected(self, listbox, row):
        self.removeAppRow = row
    
    # Create the app
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

    # Remove the app what is selected in 'Remove' window
    def removeApp_btn(self, button):
        name_quick_access = self.removeAppRow.get_child().get_text()
        removeApp(dir_config, name_quick_access)
        
        self.controls.showRemoveAppList()