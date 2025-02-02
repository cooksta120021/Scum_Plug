"""
Scum Bard: MIDI Playback Plugin

This module provides MIDI file playback functionality with custom key mapping.
"""

import os
import sys
import json
import argparse
import logging
import traceback

try:
    import mido
    import pyautogui
    import time
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

class ScumBardError(Exception):
    """Custom exception for Scum Bard errors"""
    pass

class ScumBard:
    def __init__(self, midi_file=None, track=0, keymap_path=None, log_level=logging.INFO):
        """
        Initialize ScumBard MIDI player
        
        :param midi_file: Path to MIDI file
        :param track: Track number to play (default 0)
        :param keymap_path: Custom keymap JSON file
        :param log_level: Logging level
        """
        # Configure logging
        logging.basicConfig(
            level=log_level, 
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('scum_bard.log', mode='w')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Validate input file
        if not midi_file or not os.path.exists(midi_file):
            raise ScumBardError(f"MIDI file not found: {midi_file}")
        
        self.midi_file = midi_file
        self.track = track
        
        # Default keymap
        default_keymap = {
            "c": "e", "c#": "4", "d": "r", "d#": "5", 
            "e": "t", "f": "y", "f#": "7", "g": "u", 
            "g#": "8", "a": "i", "a#": "9", "b": "0"
        }
        
        # Load custom keymap if provided
        try:
            if keymap_path and os.path.exists(keymap_path):
                with open(keymap_path, 'r') as f:
                    self.keymap = json.load(f)
                self.logger.info(f"Loaded custom keymap from {keymap_path}")
            else:
                self.keymap = default_keymap
                self.logger.info("Using default keymap")
        except json.JSONDecodeError:
            self.logger.error(f"Invalid keymap file: {keymap_path}")
            self.keymap = default_keymap

    def list_tracks(self):
        """
        List available tracks in the MIDI file
        """
        try:
            midi = mido.MidiFile(self.midi_file)
            self.logger.info(f"Tracks in {self.midi_file}:")
            for i, track in enumerate(midi.tracks):
                self.logger.info(f"Track {i}: {len(track)} messages")
        except Exception as e:
            self.logger.error(f"Error listing tracks: {e}")
            traceback.print_exc()

    def play_midi(self):
        """
        Play MIDI file using keyboard mapping
        """
        try:
            midi = mido.MidiFile(self.midi_file)
            track = midi.tracks[self.track]
            self.logger.info(f"Playing track {self.track} from {self.midi_file}")

            def midi_to_note_name(midi_number):
                """Convert MIDI note number to note name"""
                notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
                octave = (midi_number // 12) - 1
                note_index = midi_number % 12
                return f"{notes[note_index]}{octave}"

            # Use threading to prevent blocking
            import threading

            def playback_thread():
                # 5-second delay before starting
                self.logger.info("Waiting 5 seconds before starting MIDI playback...")
                time.sleep(5)
                self.logger.info("Starting MIDI playback")

                for msg in track:
                    if not msg.is_meta:
                        if msg.type == 'note_on' and msg.velocity > 0:
                            note_name = midi_to_note_name(msg.note).lower()
                            
                            if note_name in self.keymap:
                                key = self.keymap[note_name]
                                self.logger.debug(f"Pressing key: {key} for note: {note_name}")
                                pyautogui.press(key)
                    
                    # Control playback speed
                    time.sleep(msg.time * 0.1)  # Slow down playback

                self.logger.info("MIDI playback completed successfully")

            # Start playback in a separate thread
            thread = threading.Thread(target=playback_thread)
            thread.start()

        except Exception as e:
            self.logger.error(f"Error playing MIDI: {e}")
            traceback.print_exc()

def create_plugin(button=None):
    """
    Create and return a QWidget for the Scum Bard MIDI plugin
    
    :param button: Optional button that triggered the plugin (not used)
    :return: QWidget for the plugin
    """
    try:
        from PyQt5.QtWidgets import (
            QWidget, QVBoxLayout, QPushButton, 
            QLabel, QFileDialog, QMessageBox
        )
        import logging
        import sys
        
        class ScumBardPluginWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                
                # Main layout
                layout = QVBoxLayout()
                
                # Title
                title = QLabel("Scum Bard MIDI Player")
                layout.addWidget(title)
                
                # Select MIDI File Button
                select_midi_btn = QPushButton("Select MIDI File")
                select_midi_btn.clicked.connect(self.select_midi_file)
                layout.addWidget(select_midi_btn)
                
                # Play Button
                play_btn = QPushButton("Play MIDI")
                play_btn.clicked.connect(self.play_midi)
                layout.addWidget(play_btn)
                
                # Status Label
                self.status_label = QLabel("No MIDI file selected")
                layout.addWidget(self.status_label)
                
                self.setLayout(layout)
                self.midi_file = None
            
            def select_midi_file(self):
                """Open file dialog to select MIDI file"""
                # Get the absolute path to the data directory
                data_dir = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), 'data'
                ))
                
                # Ensure the data directory exists
                if not os.path.exists(data_dir):
                    QMessageBox.warning(
                        self, 
                        "Directory Not Found", 
                        f"MIDI directory not found: {data_dir}"
                    )
                    data_dir = os.path.expanduser('~')  # Fallback to user home
                
                file_path, _ = QFileDialog.getOpenFileName(
                    self, 
                    "Select MIDI File", 
                    data_dir,  # Use full path to data directory 
                    "MIDI Files (*.mid)"
                )
                
                if file_path:
                    self.midi_file = file_path
                    # Show just the filename for cleaner display
                    filename = os.path.basename(file_path)
                    self.status_label.setText(f"Selected: {filename}")
            
            def play_midi(self):
                """Play selected MIDI file"""
                if not self.midi_file:
                    QMessageBox.warning(
                        self, 
                        "Error", 
                        "Please select a MIDI file first"
                    )
                    return
                
                try:
                    bard = ScumBard(self.midi_file)
                    bard.play_midi()
                    self.status_label.setText(f"Playing: {self.midi_file}")
                except Exception as e:
                    QMessageBox.critical(
                        self, 
                        "Playback Error", 
                        f"Failed to play MIDI: {str(e)}"
                    )
        
        # Ensure QApplication exists
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        
        # Create widget
        widget = ScumBardPluginWidget()
        
        # Log and verify widget type
        logging.info(f"Created Scum Bard plugin widget: {type(widget)}")
        
        return widget
    
    except Exception as e:
        logging.error(f"Failed to create Scum Bard plugin: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Scum Bard MIDI Player")
    parser.add_argument('-f', '--file', required=True, help='MIDI file to play')
    parser.add_argument('-t', '--track', type=int, default=0, help='Track to play')
    parser.add_argument('-k', '--keymap', help='Custom keymap JSON file')
    parser.add_argument('-l', '--list-tracks', action='store_true', help='List tracks in MIDI file')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()

    # Set log level based on debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO

    try:
        bard = ScumBard(args.file, args.track, args.keymap, log_level)

        if args.list_tracks:
            bard.list_tracks()
        else:
            bard.play_midi()

    except ScumBardError as e:
        print(f"Scum Bard Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
