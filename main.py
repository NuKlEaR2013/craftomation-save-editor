import sys
from PySide6.QtWidgets import QApplication
from crafto_editor.ui.editor_window import CraftoEditor

def main():
    app = QApplication(sys.argv)
    window = CraftoEditor(app)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
