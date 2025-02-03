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
import threading

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
        Initialize ScumBard MIDI player with updated keymap
        
        :param midi_file: Path to MIDI file
        :param track: Track number to play (default 0)
        :param keymap_path: Custom keymap JSON file
        :param log_level: Logging level
        """
        logging.basicConfig(
            level=log_level, 
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('scum_bard.log', mode='w')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        if not midi_file or not os.path.exists(midi_file):
            raise ScumBardError(f"MIDI file not found: {midi_file}")
        
        self.midi_file = midi_file
        self.track = track
        
        # Updated keymap matching the specified mapping
        default_keymap = {
            "c": "z",    # Low C
            "c#": "5",   # C#
            "d": "u",    # D
            "d#": "6",   # D#
            "e": "i",    # E
            "f": "o",    # F
            "f#": "7",   # F#
            "g": "h",    # G
            "g#": "8",   # G#
            "a": "j",    # A
            "a#": "9",   # A#
            "b": "k",    # B
            "c_high": "l"  # High C
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

    def reset_character_octave(self):
        """
        Reset character to neutral octave
        """
        # Specific reset method can be added if needed
        self.logger.info("Reset character octave")

    def shift_octave(self, target_octave, current_octave):
        """
        Shift octave up or down
        
        :param target_octave: Desired octave
        :param current_octave: Current octave
        """
        if target_octave > current_octave:
            # Shift up with Left Shift
            for _ in range(target_octave - current_octave):
                pyautogui.press('shift')
                self.logger.info(f"Shifted octave up to {target_octave}")
        elif target_octave < current_octave:
            # Shift down with Left Ctrl
            for _ in range(current_octave - target_octave):
                pyautogui.press('ctrl')
                self.logger.info(f"Shifted octave down to {target_octave}")

    def get_first_octave(self, track):
        """
        Determine the first octave of the track
        
        :param track: MIDI track to analyze
        :return: Base octave of the track
        """
        octaves = []
        for msg in track:
            if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
                octave = (msg.note // 12) - 1
                octaves.append(octave)
        
        return min(octaves) if octaves else 3  # Default to octave 3 if no notes found

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
        print(f"Total track messages: {len(mido.MidiFile(self.midi_file).tracks[self.track])}")
        print(f"Current Keymap: {self.keymap}")
        
        try:
            midi = mido.MidiFile(self.midi_file)
            track = midi.tracks[self.track]
            print(f"Playing track {self.track} from {self.midi_file}")

            def midi_to_note_name(midi_number):
                """Convert MIDI note number to note name"""
                notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
                octave = (midi_number // 12) - 1
                note_index = midi_number % 12
                
                # Special handling for high C
                if notes[note_index] == 'c' and octave > 3:
                    return 'c_high'
                
                return notes[note_index]

            # Collect ALL unique notes in the track
            all_notes = {}
            
            for msg in track:
                if not msg.is_meta:
                    if msg.type in ['note_on', 'note_off'] and msg.velocity > 0:
                        note_name = midi_to_note_name(msg.note)
                        note_without_octave = ''.join([c for c in note_name if c.isalpha() or c == '#'])
                        
                        if note_name not in all_notes:
                            all_notes[note_name] = {
                                'full_name': note_name,
                                'without_octave': note_without_octave,
                                'midi_number': msg.note,
                                'mapped_key': self.keymap.get(note_without_octave, 'NO MAPPING'),
                                'count': 1
                            }
                        else:
                            all_notes[note_name]['count'] += 1
            
            # Print out ALL unique notes and their mappings
            print("\n--- ALL UNIQUE NOTES IN THE TRACK ---")
            for note, details in sorted(all_notes.items(), key=lambda x: x[1]['midi_number']):
                print(f"Note: {note}, MIDI Number: {details['midi_number']}, "
                      f"Mapped Key: {details['mapped_key']}, "
                      f"Occurrences: {details['count']}")
            
            print("\n--- NOTES THAT WILL BE PLAYED ---")
            # Actual playback logic
            def playback_thread():
                note_count = 0
                key_press_count = 0

                try:
                    for msg in track:
                        if not msg.is_meta:
                            if msg.type == 'note_on' and msg.velocity > 0:
                                note_name = midi_to_note_name(msg.note)
                                note_count += 1
                                
                                # Strip octave for keymap lookup
                                note_without_octave = ''.join([c for c in note_name if c.isalpha() or c == '#'])
                                
                                if note_without_octave in self.keymap:
                                    key = self.keymap[note_without_octave]
                                    
                                    try:
                                        pyautogui.press(key)
                                        key_press_count += 1
                                        print(f"Pressed key: {key} for note: {note_name}")
                                    except Exception as press_error:
                                        print(f"Failed to press key {key}: {press_error}")
                                else:
                                    print(f"No key mapping for note: {note_name}")

                        # Slow down to make key presses observable
                        time.sleep(msg.time * 0.1)  # Slow down playback

                    print(f"MIDI playback completed. Total Notes: {note_count}, Key Presses: {key_press_count}")

                except Exception as playback_error:
                    print(f"Error during MIDI playback: {playback_error}")
                    import traceback
                    traceback.print_exc()

            # Start playback in a separate thread
            thread = threading.Thread(target=playback_thread)
            thread.start()
            thread.join()  # Wait for thread to complete

        except Exception as e:
            print(f"Error preparing MIDI playback: {e}")
            import traceback
            traceback.print_exc()

    def play_midi_with_octave_management(self):
        """
        Play MIDI file with octave management
        """
        try:
            midi = mido.MidiFile(self.midi_file)
            track = midi.tracks[self.track]
            
            # Determine first octave
            first_octave = self.get_first_octave(track)
            current_octave = first_octave
            
            self.logger.info(f"First track octave: {first_octave}")
            
            # Reset to base octave
            self.reset_character_octave()

            def midi_to_note_name(midi_number):
                """Convert MIDI note number to note name"""
                notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
                octave = (midi_number // 12) - 1
                note_index = midi_number % 12
                
                # Special handling for high C
                if notes[note_index] == 'c' and octave > 3:
                    return 'c_high'
                
                return notes[note_index]

            def playback_thread():
                nonlocal current_octave
                note_count = 0
                key_press_count = 0

                for msg in track:
                    if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
                        note_name = midi_to_note_name(msg.note)
                        note_octave = (msg.note // 12) - 1
                        
                        # Shift octave if needed
                        if note_octave != current_octave:
                            self.shift_octave(note_octave, current_octave)
                            current_octave = note_octave
                        
                        if note_name in self.keymap:
                            key = self.keymap[note_name]
                            
                            try:
                                pyautogui.press(key)
                                key_press_count += 1
                                self.logger.info(f"Pressed key: {key} for note: {note_name} (Octave: {note_octave})")
                            except Exception as press_error:
                                self.logger.error(f"Failed to press key {key}: {press_error}")
                        
                        note_count += 1
                        time.sleep(msg.time * 0.1)  # Maintain original timing

                self.logger.info(f"MIDI playback completed. Total Notes: {note_count}, Key Presses: {key_press_count}")

            # Start playback
            thread = threading.Thread(target=playback_thread)
            thread.start()
            thread.join()

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
                    bard.play_midi_with_octave_management()
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
            bard.play_midi_with_octave_management()

    except ScumBardError as e:
        print(f"Scum Bard Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
