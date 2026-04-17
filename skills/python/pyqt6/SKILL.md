---
name: python-pyqt6
description: >
  PyQt6 patterns for desktop GUI applications.
  Trigger: When building desktop apps with PyQt6, creating windows, widgets, layouts, signals/slots.
metadata:
  author: gentleman-ai
  version: "1.0"
---

## PyQt6 App Structure (REQUIRED)

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## QMainWindow vs QWidget

| Use Case | Widget |
|----------|--------|
| App with menu bar, toolbar, status bar | `QMainWindow` |
| Dialogs, widgets, custom containers | `QWidget` |

```python
# ✅ Main Window with menu/toolbar
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMinimumSize(800, 600)
        
        # Central widget
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        
        # Menu bar
        self._create_menu_bar()
    
    def _create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Open", self.open_file)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

# ✅ Simple Widget
class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Hello"))
        self.setLayout(layout)
```

---

## Layouts (REQUIRED)

Use layouts, NEVER set fixed positions manually.

```python
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit
)

# ✅ Vertical Layout
layout = QVBoxLayout()
layout.addWidget(title_label)
layout.addWidget(input_field)
layout.addWidget(submit_button)
self.setLayout(layout)

# ✅ Horizontal Layout for button groups
button_layout = QHBoxLayout()
button_layout.addWidget(save_button)
button_layout.addWidget(cancel_button)
button_layout.addStretch()  # Push buttons to left
layout.addLayout(button_layout)

# ✅ Grid Layout for forms
grid = QGridLayout()
grid.addWidget(QLabel("Name:"), 0, 0)
grid.addWidget(name_input, 0, 1)
grid.addWidget(QLabel("Email:"), 1, 0)
grid.addWidget(email_input, 1, 1)
self.setLayout(grid)
```

---

## Signals & Slots (REQUIRED)

PyQt6 uses signals and slots for event handling.

```python
from PyQt6.QtCore import pyqtSignal

class MyWidget(QWidget):
    # Define signals
    data_changed = pyqtSignal(str)  # Emits string
    request_save = pyqtSignal(dict)  # Emits dict
    
    def __init__(self):
        super().__init__()
        button = QPushButton("Click me")
        button.clicked.connect(self.on_button_clicked)
    
    def on_button_clicked(self):
        # ✅ Emit signal instead of direct logic
        self.data_changed.emit("some_data")
    
    # ✅ Slot for external connection
    @pyqtSlot(str)
    def on_data_received(self, data: str):
        print(f"Received: {data}")
```

---

## Dialogs (REQUIRED)

Use QDialog for modal windows.

```python
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Are you sure?"))
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

# Usage
dialog = ConfirmDialog(self)
if dialog.exec() == QDialog.DialogCode.Accepted:
    self.do_action()
```

---

## File Dialogs

```python
from PyQt6.QtWidgets import QFileDialog

# ✅ Open file
filename, _ = QFileDialog.getOpenFileName(
    self,
    "Open File",
    "",
    "Text Files (*.txt);;All Files (*)"
)

# ✅ Save file
filename, _ = QFileDialog.getSaveFileName(
    self,
    "Save File",
    "",
    "Text Files (*.txt);;All Files (*)"
)

# ✅ Select directory
directory = QFileDialog.getExistingDirectory(self, "Select Directory")
```

---

## Qt Designer Integration (OPTIONAL)

For complex UIs, use Qt Designer and convert `.ui` to Python:

```bash
# Convert .ui to Python
pyuic6 designer.ui -o ui_designer.py

# Usage
from ui_designer import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
```

---

## Resources

- https://doc.qt.io/qt-6/index.html
- https://www.pythonguis.com/pyqt6-tutorial/
