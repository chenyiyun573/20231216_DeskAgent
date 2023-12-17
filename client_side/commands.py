import ctypes
from ctypes import wintypes

# Function to move the mouse
def move_mouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

# Function to perform a mouse click
def click_mouse(left=True):
    if left:
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left click down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left click up
    else:
        ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)  # Right click down
        ctypes.windll.user32.mouse_event(16, 0, 0, 0, 0)  # Right click up

# Define necessary structures for SendInput
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR)]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [("type", wintypes.DWORD), ("_input", _INPUT)]

# Constants for input type
INPUT_KEYBOARD = 1

# Function to simulate a key press
def press_key(hexKeyCode):
    input_struct = INPUT(type=INPUT_KEYBOARD,
                         ki=KEYBDINPUT(wVk=hexKeyCode,
                                       dwFlags=0))
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))

# Function to simulate a key release
def release_key(hexKeyCode):
    input_struct = INPUT(type=INPUT_KEYBOARD,
                         ki=KEYBDINPUT(wVk=hexKeyCode,
                                       dwFlags=2))  # KEYEVENTF_KEYUP = 0x0002
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))


# Function to type a string
def type_string(text):
    for char in text:
        keycode = ord(char)
        press_key(keycode)
        release_key(keycode)