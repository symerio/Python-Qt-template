from qtpy import QtCore
from gui_template.core import GUIMainWindow


def test_main_window(qtbot):
    app = GUIMainWindow()
    app.show()
    qtbot.mouseClick(app.tabs['Main']['plot_btn']['qtobj'],
                     QtCore.Qt.LeftButton)
    assert app.fig is not None
