import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter,
    QListWidget, QListWidgetItem, QLabel, QSlider,
    QLineEdit, QPushButton, QStatusBar, QVBoxLayout,
    QHBoxLayout, QFrame, QTextBrowser, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from qt_material import apply_stylesheet

from crafto_editor.fileio import (
    get_save_dir,
    list_save_files,
    read_progression_points,
    write_progression_points
)

class CraftoEditor(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.setWindowTitle("🚀 Craftomation101 Editor")
        self.resize(1000, 600)
        self.offset = None
        self.current_value = None
        self.selected_file = None

        # Apply theme & font
        apply_stylesheet(app, theme='dark_blue.xml')
        font = app.font()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        app.setFont(font)

        # Layout splitter
        splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(splitter)

        # — Left Nav —
        nav = QFrame()
        nav.setFrameShape(QFrame.StyledPanel)
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(12, 12, 12, 12)

        # Toolbar
        tb = QHBoxLayout()
        btn_refresh = QPushButton("↻")
        btn_refresh.clicked.connect(self.reload_files)
        tb.addWidget(btn_refresh)
        tb.addWidget(QPushButton("⚙️"))  # stub
        tb.addStretch()
        nav_layout.addLayout(tb)

        # Search
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search save files…")
        self.search.textChanged.connect(self.filter_files)
        nav_layout.addWidget(self.search)

        # File list
        self.files = QListWidget()
        self.files.currentItemChanged.connect(self.on_file_select)
        nav_layout.addWidget(self.files)
        splitter.addWidget(nav)
        nav.setMaximumWidth(300)

        # — Right Editor —
        edit = QFrame()
        edit.setFrameShape(QFrame.StyledPanel)
        edit_layout = QVBoxLayout(edit)
        edit_layout.setContentsMargins(20, 20, 20, 20)
        splitter.addWidget(edit)

        # Description
        desc = QTextBrowser()
        desc.setHtml(
            "<h3>What this does</h3>"
            "<p>This tool lets you tweak your <b>progressionPoints</b> "
            "in any Craftomation101 save file. Use the slider or numeric entry "
            "to adjust your in‑game progression between <b>1</b> and <b>20</b>, "
            "then click Save.</p>"
        )
        desc.setFixedHeight(120)
        desc.setFrameShape(QFrame.NoFrame)
        edit_layout.addWidget(desc)

        # Header & Current
        header = QLabel("🧮 Edit progressionPoints")
        header.setStyleSheet("font-size: 18pt; color: #ECEFF4;")
        edit_layout.addWidget(header)

        self.current = QLabel("Current Value: <b>—</b>")
        self.current.setStyleSheet("font-size: 14pt; color: #D8DEE9;")
        edit_layout.addWidget(self.current)

        # Slider + Entry
        row = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 20)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.on_slider_change)
        row.addWidget(self.slider, 3)

        self.val_in = QLineEdit()
        self.val_in.setMaximumWidth(60)
        self.val_in.returnPressed.connect(self.on_entry_change)
        row.addWidget(self.val_in, 1)
        edit_layout.addLayout(row)

        # Spinner (progress bar) hidden initially
        self.spinner = QProgressBar()
        self.spinner.setRange(0, 0)
        self.spinner.setVisible(False)
        edit_layout.addWidget(self.spinner)

        # Buttons
        btns = QHBoxLayout()
        btns.addStretch()
        self.reset_btn = QPushButton("⟲ Reset")
        self.reset_btn.clicked.connect(self.on_reset)
        btns.addWidget(self.reset_btn)
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.on_save)
        btns.addWidget(self.save_btn)
        edit_layout.addLayout(btns)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Load initial file list
        self.reload_files()
        self.enable_controls(False)

    def enable_controls(self, enabled: bool):
        self.slider.setEnabled(enabled)
        self.val_in.setEnabled(enabled)
        self.save_btn.setEnabled(enabled)
        self.reset_btn.setEnabled(enabled)

    # — NAVIGATION —
    def reload_files(self):
        self.files.clear()
        for fname in list_save_files():
            self.files.addItem(QListWidgetItem(fname))

    def filter_files(self, term: str):
        for i in range(self.files.count()):
            item = self.files.item(i)
            item.setHidden(term.lower() not in item.text().lower())

    # — FILE LOADING —
    def on_file_select(self, current: QListWidgetItem, _):
        if not current:
            return
        fname = current.text()
        path = os.path.join(get_save_dir(), fname)
        self.selected_file = path
        self.spinner.setVisible(True)
        QTimer.singleShot(100, lambda: self.load_file(path, fname))

    def load_file(self, path: str, fname: str):
        try:
            val, off = read_progression_points(path)
            if val is None:
                raise ValueError("progressionPoints not found")

            self.offset = off
            self.current_value = val
            self.current.setText(f"Current Value: <b>{val:.4f}</b>")

            disp = max(1, min(20, int(round(val))))
            self.slider.setValue(disp)
            self.val_in.setText(str(disp))

            self.enable_controls(True)
            self.status.showMessage(f"Loaded '{fname}'", 3000)

        except ValueError as ve:
            self.current.setText(
                f"<span style='color:#BF616A;'><b>Error:</b> {ve}</span>"
            )
            self.enable_controls(False)
            self.status.showMessage(f"ERROR: {ve}", 5000)

        except Exception as e:
            self.current.setText(
                f"<span style='color:#BF616A;'><b>Unexpected:</b> {e}</span>"
            )
            self.enable_controls(False)
            self.status.showMessage(f"ERROR: {e}", 5000)

        finally:
            self.spinner.setVisible(False)

    # — SYNCHRONIZATION —
    def on_slider_change(self, v: int):
        self.val_in.setText(str(v))

    def on_entry_change(self):
        try:
            v = int(self.val_in.text())
            if 1 <= v <= 20:
                self.slider.setValue(v)
        except ValueError:
            pass

    # — SAVE / RESET —
    def on_save(self):
        if not self.selected_file or self.offset is None:
            self.status.showMessage("No file loaded!", 5000)
            return
        try:
            new_v = float(self.val_in.text())
            write_progression_points(self.selected_file, self.offset, new_v)
            self.current_value = new_v
            self.current.setText(f"Current Value: <b>{new_v:.4f}</b>")
            self.status.showMessage(f"Saved {new_v:.4f} ✔", 3000)
        except Exception as e:
            self.status.showMessage(f"SAVE FAILED: {e}", 5000)

    def on_reset(self):
        if self.current_value is not None:
            disp = max(1, min(20, int(round(self.current_value))))
            self.slider.setValue(disp)
            self.val_in.setText(str(disp))
            self.status.showMessage("Reverted to last loaded value", 3000)
