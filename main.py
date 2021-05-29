
from controller import Handler
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("project.glade")

    builder.connect_signals(Handler(builder))
    window = builder.get_object("Main_window")
    window.set_default_size(500, 100)
    window.show_all()

    # Provisional
    builder.get_object('app_box_3').hide()
    builder.get_object('app_box_4').hide()

    Gtk.main() 