
import os
import sys

from PyQt5.QtWidgets import QApplication

from interfaces.SRDialog import SRDialog

UI_FILES_PATH = "interfaces"


def init():
    ui_files = [os.path.join(UI_FILES_PATH, x) for x in os.listdir(UI_FILES_PATH) if x.endswith(".ui")]
    for ui_file in ui_files:
        ui_out_name = os.path.join(UI_FILES_PATH, "UI_%s.py" % os.path.basename(ui_file).split(".")[0])
        cmd = "pyuic5 -o %s %s" % (ui_out_name, ui_file)
        print(cmd)
        os.system(cmd)


def main():
    init()
    app = QApplication(sys.argv)
    sr_dialog = SRDialog()
    sr_dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()