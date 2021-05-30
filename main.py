from Controller.controller import Signals, Controls
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("View/project.glade")
    
    signals = Signals(builder)
    controls = Controls(builder)
    builder.connect_signals(signals)
    window = builder.get_object("Main_window")
    window.set_default_size(500, 100)
    controls.showRemoveAppList()
    window.show_all()

    # Provisional
    builder.get_object('app_box_3').hide()
    builder.get_object('app_box_4').hide()

    Gtk.main()