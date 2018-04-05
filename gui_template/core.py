import sys
import traceback

from qtpy import QtWidgets
from SiQt.dep_resolv import sync_gui, calculate_dependencies
from SiQt.widgets import (DebugInfoWidget,)

from .definitions import GUIMainWindowBase,  show_figure

# handle exceptions inside the application
sys.excepthook = traceback.print_exception


class GUIMainWindow(GUIMainWindowBase):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle('Qt GUI template')

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        self.widgets = {}
        for key in ['debug']:
            self.widgets[key] = None

    @sync_gui(update=['original'], view_mode='original')
    def on_open_datafile(self, state=None):
        file_choices = "All Files (*)"

        path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                     'Load file', '',
                                                     file_choices, None,)
        path = str(path)
        if not path:
            return

    def on_draw(self):
        """Draw the figure
        """
        ax = self.ax

        # clear the axes and redraw the plot anew
        ax.axes.set_frame_on(False)
        ax.clear()
        show_figure(self)(True)

        # self.ax.set_aspect('equal')
        self.ax.plot([0, 1, 2, 3], [1, 2, 4, 2])

        self.fig.tight_layout()

        self.canvas.flush_events()
        self.canvas.draw()

    def update_flag_checkbox(self, flag, tab_key, obj_key):
        ctab = self.tabs[tab_key]
        value = ctab[obj_key].value
        self.set_dep_flag_recursive(flag, value)
        calculate_dependencies(self, verbose=False)

    def on_debug_information(self):
        if self.widgets['debug'] is not None:
            self.widgets['debug'].close()
        self.widgets['debug'] = DebugInfoWidget(self)
        self.widgets['debug'].show()
