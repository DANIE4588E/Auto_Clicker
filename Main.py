from pynput import mouse
import ctypes
import threading

click_detected = False

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

MOUSE_LEFTDOWN = 0x0002
MOUSE_LEFTUP = 0x0004

def on_click(x, y, button, pressed):
    global click_detected
    if button == mouse.Button.right and pressed:
        click_detected = not click_detected 

def perform_click():
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, MOUSE_LEFTDOWN, 0, None)
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    ii_.mi = MouseInput(0, 0, 0, MOUSE_LEFTUP, 0, None)
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def click_thread():
    while True:
        if click_detected:
            perform_click()

listener = mouse.Listener(on_click=on_click)
listener.start()

thread = threading.Thread(target=click_thread)
thread.start()
