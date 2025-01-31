import os
import sys
from PyQt5.QtWidgets import (QPushButton, QSizePolicy, QMenu, QMessageBox, QApplication)
from PyQt5.QtCore import Qt

class PluginButton(QPushButton):
    def __init__(self, plugin_name, overlay):
        super().__init__(plugin_name)
        
        # Store plugin information
        self.plugin_name = plugin_name
        self.overlay = overlay
        self.active_plugin = None
        
        # Disable dragging
        self.setMouseTracking(False)
        
        # Make button non-movable and resize with parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Button styling
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 100, 200, 230);
                color: white;
                border: 3px solid white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: rgba(70, 120, 220, 250);
            }
        """)
        
        # Context menu for button
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # If not dragging, toggle plugin
            if not self.active_plugin:
                self.active_plugin = self.overlay.load_plugin(self.plugin_name, self)
                
                # Change button style when plugin is loaded
                if self.active_plugin:
                    self.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(0, 255, 0, 230);
                            color: white;
                            border: 3px solid white;
                            border-radius: 15px;
                            font-weight: bold;
                            font-size: 14px;
                            text-transform: uppercase;
                        }
                    """)
            else:
                # Toggle visibility of active plugin
                if self.active_plugin.isVisible():
                    self.active_plugin.hide()
                    self.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(50, 100, 200, 230);
                            color: white;
                            border: 3px solid white;
                            border-radius: 15px;
                            font-weight: bold;
                            font-size: 14px;
                            text-transform: uppercase;
                        }
                    """)
                else:
                    self.active_plugin.show()
                    self.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(0, 255, 0, 230);
                            color: white;
                            border: 3px solid white;
                            border-radius: 15px;
                            font-weight: bold;
                            font-size: 14px;
                            text-transform: uppercase;
                        }
                    """)
        
        super().mousePressEvent(event)
    
    def show_context_menu(self, pos):
        # Create context menu
        context_menu = QMenu(self)
        
        # Add Check for Updates action
        update_action = context_menu.addAction("Check for Updates")
        update_action.triggered.connect(self.overlay.check_for_updates)
        
        # Add Exit Application action
        exit_action = context_menu.addAction("Exit Application")
        exit_action.triggered.connect(QApplication.quit)
        
        # Show menu at global position
        context_menu.exec_(self.mapToGlobal(pos))
    
    def exit_plugin(self):
        # Close and destroy the active plugin if exists
        if self.active_plugin:
            self.active_plugin.close()
            self.active_plugin.deleteLater()  # Ensure complete destruction
            self.active_plugin = None
            
            # Reset button style
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 100, 200, 230);
                    color: white;
                    border: 3px solid white;
                    border-radius: 15px;
                    font-weight: bold;
                    font-size: 14px;
                    text-transform: uppercase;
                }
            """)
