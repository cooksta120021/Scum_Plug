from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QMenu, QApplication, QAction)
from PyQt5.QtCore import Qt

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create title label
        self.title_label = QLabel("ScumPlug Overlay")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: black;
                font-weight: bold;
            }
        """)
        
        # Add title label to layout
        layout.addWidget(self.title_label)
        
        # Set layout
        self.setLayout(layout)
        
        # Enable custom context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Make widget draggable
        self.mousePressEvent = self.mouse_press
        self.mouseMoveEvent = self.mouse_move
    
    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            # Store the current mouse position
            self.drag_start_position = event.globalPos()
            # Get the parent window
            self.parent_window = self.parent().parent()
    
    def mouse_move(self, event):
        if event.buttons() == Qt.LeftButton:
            # Calculate the distance moved
            current_pos = event.globalPos()
            diff = current_pos - self.drag_start_position
            
            # Move the parent window
            new_pos = self.parent_window.pos() + diff
            self.parent_window.move(new_pos)
            
            # Update the start position
            self.drag_start_position = current_pos
    
    def show_context_menu(self, pos):
        # Delegate to the parent ScumPlug window's context menu method
        scum_plug = self.parent().parent()
        scum_plug.show_context_menu(pos)
