from Controller.controller import Signals
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Create the main window
def createMainWindow():
    builder = Gtk.Builder()
    builder.add_from_file("View/project.glade")

    signals = Signals(builder)
    builder.connect_signals(signals)

    main_window = builder.get_object("Main_window") 
    main_window.show_all()
  

if __name__ == '__main__':

    createMainWindow()
    Gtk.main()